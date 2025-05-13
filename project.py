import csv
import os
from datetime import datetime, timedelta

DATA_FILE = "user_data.csv"
HISTORY_FILE = "calorie_history.csv"

def main():
    name, weight, height, daily_calories, bmi, last_missed_calories = get_user_data()
    print(f"Hello {name}, Welcome back to your Nutritional Assistant!")

    if weight and height:
        print(f"Found previous data: Weight: {weight} kg, Height: {height} cm")
        if daily_calories:
            print(f"Your daily calorie intake was estimated to be {daily_calories:.0f} kcal.")
        if bmi:
            print(f"Your BMI was {bmi:.1f}")
        if last_missed_calories is not None:
            print(f"Last time you missed {abs(last_missed_calories):.0f} kcal from your target.")

        choice = input("Do you want to update your data? (y/n) ").strip().lower()
        if choice == "y":
            weight, height, daily_calories, bmi = update_user_data(name)
        elif choice != "n":
            print("Invalid choice. Proceeding with current data.")
    else:
        print("No previous data found. Let's enter your details.")
        weight, height, daily_calories, bmi = update_user_data(name)

    bmi = calculate_bmi(weight, height)
    if bmi is not None:
        print(f"Your BMI is {bmi:.1f}")
        if bmi < 18.5:
            print("You are underweight. Consider increasing calorie intake.")
        elif bmi <= 24.9:
            print("You are in a healthy range. Great job!")
        elif bmi <= 29.9:
            print("You are overweight. Consider balancing your diet.")
        else:
            print("You are in the obese range. Exercise and diet are recommended.")

    if daily_calories is None:
        daily_calories = calculate_daily_calories(weight, height)

    print(f"Your recommended daily calorie intake is: {daily_calories:.0f} kcal")
    track_calories(name, daily_calories, weight, height)

def track_calories(name, daily_calories, weight, height):
    today = datetime.now().strftime("%Y-%m-%d")
    previous_calories = get_today_calories(name, today)

    try:
        if previous_calories > 0:
            print(f"Last time you added {previous_calories:.0f} kcal for today.")

        new_calories = float(input("Enter the calories you consumed today: "))
        total_calories = previous_calories + new_calories
        difference = total_calories - daily_calories

        print(f"Today you've consumed a total of {total_calories:.0f} kcal.")

        # Check if the user is underweight
        bmi = calculate_bmi(weight, height)  # Assuming weight and height are available globally or passed as arguments
        if bmi is not None and bmi < 18.5:
            if difference > 0:
                print(f"👍 Good job! You've consumed {abs(difference):.0f} kcal more than your target today. Keep it up!")
            elif difference < 0:
                print(f"You've consumed {abs(difference):.0f} kcal less than your target today. Try to eat a bit more!")
            else:
                print("You've met your calorie target exactly today. Great job!")
        else:
            if difference > 0:
                print(f"⚠️ Attention: You've consumed {abs(difference):.0f} kcal more than your target today!")
            elif difference < 0:
                print(f"You've consumed {abs(difference):.0f} kcal less than your target today.")
            else:
                print("You've met your calorie target exactly today. Great job!")

        save_missed_calories(name, difference)
        save_calorie_history(name, today, total_calories)

        compare_with_last_week(name, today, total_calories)
        track_streak(name, today)

        print("Keep up the good work! Your progress is saved.")
    except ValueError:
        print("Please enter a valid number.")

def get_today_calories(name, today):
    if not os.path.exists(HISTORY_FILE):
        return 0
    with open(HISTORY_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name and row[1] == today:
                return float(row[2])
    return 0

def save_missed_calories(name, missed_calories):
    rows = []
    updated = False

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            rows = list(csv.reader(file))

    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if row and row[0].lower() == name.lower():
                row[5] = missed_calories
                updated = True
            writer.writerow(row)
        if not updated:
            writer.writerow([name, "", "", "", "", missed_calories])

def save_calorie_history(name, date, calories):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Calories"])

    with open(HISTORY_FILE, "r") as file:
        existing = list(csv.reader(file))

    with open(HISTORY_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        updated = False
        for row in existing:
            if row and row[0] == name and row[1] == date:
                row[2] = calories
                updated = True
            writer.writerow(row)
        if not updated:
            writer.writerow([name, date, calories])

def compare_with_last_week(name, today_str, today_calories):
    last_week_date = (datetime.strptime(today_str, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    if not os.path.exists(HISTORY_FILE):
        return

    with open(HISTORY_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name and row[1] == last_week_date:
                last_week_calories = float(row[2])
                diff = today_calories - last_week_calories
                if diff > 0:
                    print(f"You consumed {abs(diff):.0f} kcal more than the same day last week.")
                elif diff < 0:
                    print(f"You consumed {abs(diff):.0f} kcal less than the same day last week.")
                else:
                    print("Your calorie intake is the same as last week.")
                return

def track_streak(name, today_str):
    streak = 1
    if not os.path.exists(HISTORY_FILE):
        return

    today = datetime.strptime(today_str, "%Y-%m-%d")
    dates = []
    with open(HISTORY_FILE, "r") as file:
        for row in csv.reader(file):
            if row and row[0] == name:
                dates.append(row[1])
    dates = sorted(set(datetime.strptime(d, "%Y-%m-%d") for d in dates), reverse=True)
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            streak += 1
        else:
            break

    print(f"You have logged your calories for {streak} day(s) in a row!")

def get_user_data():
    if os.path.exists(DATA_FILE):
        name = input("Enter your name: ").strip()
        with open(DATA_FILE, "r") as file:
            for row in csv.reader(file):
                if row and row[0].lower() == name.lower():
                    weight = float(row[1]) if row[1] else None
                    height = float(row[2]) if row[2] else None
                    daily_calories = float(row[3]) if row[3] else None
                    bmi = float(row[4]) if row[4] else None
                    missed_calories = float(row[5]) if row[5] else None
                    return name, weight, height, daily_calories, bmi, missed_calories
        print(f"No user found with the name '{name}'. Creating a new profile.")
    else:
        print("No existing data found. Creating a new profile.")

    name = input("Create new profile: ")
    return name, None, None, None, None, None

def update_user_data(name):
    try:
        weight = float(input("Enter your weight (kg): "))
        height = float(input("Enter your height (cm): "))
        daily_calories = calculate_daily_calories(weight, height)
        bmi = calculate_bmi(weight, height)

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Weight", "Height", "Daily Calories", "BMI", "Missed Calories"])

        rows = []
        updated = False
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                rows = list(csv.reader(file))

        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                if row and row[0].lower() == name.lower():
                    row = [name, weight, height, daily_calories, bmi, 0]
                    updated = True
                writer.writerow(row)
            if not updated:
                writer.writerow([name, weight, height, daily_calories, bmi, 0])

        return weight, height, daily_calories, bmi
    except ValueError:
        print("Invalid input. Try again.")
        return update_user_data(name)

def calculate_bmi(weight, height):
    try:
        return 1.3 * weight / (height / 100) ** 2.5
    except:
        return None

def calculate_daily_calories(weight, height):
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age.")
        return None

    gender = input("Enter your gender (m/f): ").strip().lower()
    if gender not in ("m", "f"):
        print("Invalid gender.")
        return None

    print("Activity levels:\n1. Sedentary\n2. Light\n3. Moderate\n4. Active\n5. Very active")
    activity = input("Choose activity level (1-5): ").strip()
    factors = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725, "5": 1.9}
    if activity not in factors:
        print("Invalid activity level.")
        return None

    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == 'm' else -161)
    factor = factors[activity]
    return bmr * factor

main()



