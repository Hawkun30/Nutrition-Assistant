# Nutrition Assistant

## Description

**Nutrition Assistant** is a simple but helpful command-line tool that helps you track your daily food intake, calculate your Body Mass Index (BMI), and receive personalized diet suggestions. The assistant is lightweight, does not require an internet connection, and stores all data locally using CSV files. It is ideal for users who prefer privacy and simplicity over complex nutrition apps.

When the program starts, it asks for your personal details—name, weight, height, age and daily activity level—and calculates your recommended daily calorie intake using the Mifflin-St Jeor equation. From there, it allows you to:

- Log calories consumed daily
- Track whether you’re meeting or missing your daily goals
- Calculate and interpret your BMI
- Save daily records automatically
- Track your weekly streak and progress over time

All data is stored in CSV files that can be opened or edited manually if needed.

---

## Features

- **BMI Calculator**
  Enter your height and weight to calculate your Body Mass Index using a modified formula. Get real-time health advice based on the result.

- **Calorie Tracker**
  Track daily calorie intake and compare it to your recommended target. Records how much you’re above or below.

- **Meal Logging**
  Log calories from breakfast, lunch, dinner, or snacks.

- **Daily & Weekly Tracking**
  Each entry is stored with the current date, and users can see their progress throughout the week.

- **Diet Suggestions**
  Basic suggestions based on calorie performance, such as “You’re under your target, try eating a healthy snack.”

- **CSV Storage**
  Data is stored in `user_data.csv` and `calorie_history.csv`. No cloud, no login, fully offline.

---

## Files

- `project.py`
  Main application file. Contains the main function and all logic for calculating BMI, tracking calories, and updating user data.

- `test_project.py`
  Contains unit tests written using `pytest` to test key functions like BMI calculation, calorie logging, and file handling.

- `requirements.txt`
  Lists required Python packages. Currently, only `pytest` is required.

- `user_data.csv`
  Stores user profiles including name, weight, height, BMI, and calorie stats.

- `calorie_history.csv`
  Logs daily calorie intake with timestamps.

- `README.md`
  You’re reading it! Explains project purpose, structure, and usage.

---

## How to Run

To start the program:

```bash
python project.py
```

To run tests:

`pytest test_project.py`

Make sure you have `pytest` installed:

`pip install -r requirements.txt`

## How It Works

### BMI Calculation

The Body Mass Index (BMI) is calculated using a slightly modified version of the standard formula:

`BMI = 1.3 * weight / (height / 100) ** 2.5`

This adjusted formula is known as the **Smart BMI** and provides a more accurate estimate across a range of body types compared to the traditional BMI formula:

`BMI = weight / (height / 100) ** 2`

The result is used to categorize the user's weight status (underweight, normal, overweight, obese) and provide basic health advice.

----------

### Daily Calorie Needs

Daily caloric needs are calculated using the **Mifflin-St Jeor Equation**, which estimates Basal Metabolic Rate (BMR) and multiplies it by an activity factor:


`BMR (men) = 10 * weight + 6.25 * height - 5 * age + 5 `

 `BMR (women) = 10 * weight + 6.25 * height - 5 * age - 161`

This value is then adjusted by the user’s activity level:
| Activity Level        | Factor |
| --------------------- | ------ |
| Sedentary (0)         | 1.2    |
| Lightly active (1)    | 1.375  |
| Moderately active (2) | 1.55   |
| Very active (3)       | 1.725  |




`Calories = BMR * activity_factor`

This gives an estimate of how many calories the user should consume daily to maintain their current weight.

----------

### Calorie Tracking Logic

Each day, the user is prompted to input how many calories they consumed. The difference between consumed and recommended calories is stored, allowing the app to track if the user consistently under- or overshoots their target. A CSV log keeps historical data for progress review.

## Why This Project?

I wanted to build something practical that I (or others) could actually use. Most nutrition apps require signups, ads, or subscriptions. This project provides a free, private alternative that runs locally on your machine, is fully customizable, and teaches you a bit about how nutrition works along the way.

I also used it as a way to reinforce my understanding of Python, file handling, input validation, and testing with `pytest`. It’s not just functional—it’s educational.

## Suggestions?

Feel free to fork this on GitHub or suggest features. I’m always happy to hear feedback!
