import pytest
import os
import csv
from io import StringIO
import sys

# Importing functions from your script
from project import (
    calculate_bmi,
    calculate_daily_calories,
    get_user_data,
    save_missed_calories,
    save_calorie_history,
    track_calories
)

@pytest.fixture
def clean_files():
    """Fixture to clean up data files before and after tests."""
    if os.path.exists("user_data.csv"):
        os.remove("user_data.csv")
    if os.path.exists("calorie_history.csv"):
        os.remove("calorie_history.csv")
    yield
    # Clean up after test
    if os.path.exists("user_data.csv"):
        os.remove("user_data.csv")
    if os.path.exists("calorie_history.csv"):
        os.remove("calorie_history.csv")


def test_calculate_bmi_valid():
    """Test the BMI calculation function with valid inputs."""
    weight = 70  # kg
    height = 175  # cm
    expected_bmi = 1.3 * weight / (height / 100) ** 2.5
    assert pytest.approx(calculate_bmi(weight, height), 0.01) == expected_bmi


def test_calculate_bmi_invalid():
    """Test the BMI calculation function with invalid inputs (e.g., height = 0)."""
    weight = 70
    height = 0  # Invalid height
    assert calculate_bmi(weight, height) is None


def test_calculate_daily_calories_valid(monkeypatch):
    """Test daily calorie calculation with valid input."""
    inputs = iter(["25", "m", "2"])  # Simulated user input
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    weight = 70
    height = 175
    expected_bmr = 10 * weight + 6.25 * height - 5 * 25 + 5  # BMR for men
    expected_calories = expected_bmr * 1.375  # Lightly active activity factor
    assert pytest.approx(calculate_daily_calories(weight, height), 0.01) == expected_calories


def test_get_user_data_existing(clean_files, monkeypatch):
    """Test if user data is fetched correctly from the CSV file."""
    name = "John Doe"
    with open("user_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, 70, 175, 2500, 24.5, 100])

    # Simula l'input dell'utente per il nome
    monkeypatch.setattr("builtins.input", lambda _: name)

    # Ora testa se i dati vengono caricati correttamente
    user_data = get_user_data()
    assert user_data[0] == name
    assert user_data[1] == 70
    assert user_data[2] == 175
    assert user_data[3] == 2500
    assert user_data[4] == 24.5
    assert user_data[5] == 100


def test_save_missed_calories(clean_files):
    """Test saving missed calories to the CSV file."""
    name = "John Doe"
    missed_calories = -200
    save_missed_calories(name, missed_calories)

    # Check if the missed calories value is saved in the CSV file
    with open("user_data.csv", "r") as file:
        rows = list(csv.reader(file))
        for row in rows:
            if row[0].lower() == name.lower():
                assert float(row[5]) == missed_calories


def test_save_calorie_history(clean_files):
    """Test saving calorie history."""
    name = "John Doe"
    today = "2025-05-11"
    calories = 2200
    save_calorie_history(name, today, calories)

    # Check if the calorie history is saved correctly
    with open("calorie_history.csv", "r") as file:
        rows = list(csv.reader(file))
        for row in rows:
            if row[0].lower() == name.lower() and row[1] == today:
                assert float(row[2]) == calories


def test_calorie_tracking_logic(clean_files):
    """Test the calorie tracking logic."""
    name = "John Doe"
    daily_calories = 2500

    # Using StringIO to mock input/output
    user_input = "2200\n"  # User's calories input for the day
    sys.stdin = StringIO(user_input)

    # Call the track_calories function and check the output
    track_calories(name, daily_calories)

    # Check that the file was updated
    with open("calorie_history.csv", "r") as file:
        rows = list(csv.reader(file))
        found = any(row[0].lower() == name.lower() for row in rows)
        assert found

    # Restore sys.stdin
    sys.stdin = sys.__stdin__


if __name__ == "__main__":
    pytest.main()
