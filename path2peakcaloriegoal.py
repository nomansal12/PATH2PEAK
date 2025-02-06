import tkinter as tk
from tkinter import messagebox
import openai
import os

# Set your OpenAI API key
openai.api_key = "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"


def poundstokg(body_weight):
    kilograms = body_weight * 0.453592
    return kilograms


def feetandinchestocm(feet, inches):
    cmvalue = (feet * 30.48) + (inches * 2.54)
    return cmvalue


def bmrformen(kg, cm, age):
    bmr = 10 * kg + 6.25 * cm - 5 * age + 5
    return bmr


def bmrforwomen(kg, cm, age):
    bmr = 10 * kg + 6.25 * cm - 5 * age - 161
    return bmr


##def calculate_bmi(kg, cm):
    # Convert height from cm to meters
    #height_m = cm / 100
    #bmi = kg / (height_m ** 2)
    #return bmi


##def bmivalidate(bmi):
    ##if bmi < 18.5:
        ##return "you will be in the category of underweight."
    ##elif 18.5 <= bmi < 24.9:
        ##return "you have a normal weight."
    ##elif 25 <= bmi < 29.9:
        ##return "you will be in the category of overweight."
    ##else:
        ##return "you will be in the category of obese."


# Function to generate a meal plan based on the calories
def generate_meal_plan(calories):
    prompt = f"Create a daily meal plan for {calories} calories. The plan should include breakfast, lunch, and dinner. Snacks can be added if needed. " \
             "Please list the food items and the estimated calories for each meal."

    try:
        # Request meal plan from OpenAI using the correct API for chat models
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use 'gpt-4' if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates personalized meal plans."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )

        # Return the generated meal plan
        meal_plan = response['choices'][0]['message']['content'].strip()
        return meal_plan
    except Exception as e:
        return f"Error generating meal plan: {str(e)}"


# Function to generate a workout plan based on the user's fitness goal
def generate_workout_plan(calories, goal, activity_level):
    prompt = f"Create a personalized workout plan for someone who needs {calories} calories per day. " \
             f"The goal is to {goal}. Based on an activity level of {activity_level}, include exercises for chest, back, shoulders, biceps, triceps, and legs. " \
             "Provide exercises, sets, reps, and time for each workout session."

    try:
        # Request workout plan from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use 'gpt-4' if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates personalized workout plans."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )

        # Return the generated workout plan
        workout_plan = response['choices'][0]['message']['content'].strip()
        return workout_plan
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"


def main():
    # Input Validation for Age
    while True:
        try:
            age = int(input("Enter your age: "))
            if age <= 0:
                print("Age must be a positive number.")
            else:
                break
        except ValueError:
            print("Please enter a valid integer for age.")

    # Input Validation for Sex
    while True:
        sex = input("Enter your sex (M/F): ").strip().upper()
        if sex in ['M', 'F']:
            break
        else:
            print("Please enter 'M' for male or 'F' for female.")

    # Input Validation for Body Weight
    while True:
        try:
            body_weight = float(input("Enter your body weight in pounds: "))
            if body_weight <= 0:
                print("Weight must be a positive number.")
            else:
                break
        except ValueError:
            print("Please enter a valid number for weight.")

    # Input Validation for Height (in feet and inches)
    while True:
        height = input("Enter your height in feet and inches (e.g., 5'10): ").strip()
        try:
            feet, inches = height.split("'")
            inches = inches.replace('"', '')
            feet = int(feet)
            inches = int(inches)
            if feet <= 0 or inches < 0:
                print("Height values must be positive. Inches cannot be negative.")
            else:
                break
        except ValueError:
            print("Please enter your height in the correct format (e.g., 5'10).")

    kg = poundstokg(body_weight)

    cm = feetandinchestocm(feet, inches)

    if sex == "M":
        bmr = bmrformen(kg, cm, age)
    elif sex == "F":
        bmr = bmrforwomen(kg, cm, age)

    # Input Validation for Activity Level
    while True:
        answer = input(
            "Choose your activity level:\n"
            "1. Little to no exercise \n"
            "2. Light exercise (1-3 days/week)\n"
            "3. Moderate exercise (3-5 days/week)\n"
            "4. Heavy exercise (6-7 days a week)\n"
            "5. Very heavy exercise (twice a day)\n"
            "Enter the number: ")

        if answer == "1":
            tdee = bmr * 1.2
            activity_level = "Little to no exercise"
            break
        elif answer == "2":
            tdee = bmr * 1.375
            activity_level = "Light exercise"
            break
        elif answer == "3":
            tdee = bmr * 1.55
            activity_level = "Moderate exercise"
            break
        elif answer == "4":
            tdee = bmr * 1.725
            activity_level = "Heavy exercise"
            break
        elif answer == "5":
            tdee = bmr * 1.9
            activity_level = "Very heavy exercise"
            break
        else:
            print("Invalid choice. Please choose a valid activity level.")

    # Handle weight goal input with error checking for "gain", "lose", and "maintain"
    while True:
        goal = input(
            "Do you want to gain, lose, or maintain your weight in a month? (gain/lose/maintain): ").strip().lower()

        if goal in ["gain", "lose", "maintain"]:
            break  # Exit the loop if a valid input is entered
        else:
            print("Invalid input. Please enter 'gain', 'lose', or 'maintain'.")

    if goal == "gain":
        while True:
            try:
                weight_gain_change = float(input("How many pounds would you like to gain in a month? "))
                if weight_gain_change <= 0:
                    print("Gain must be a positive number.")
                else:
                    calorie_surplus = (weight_gain_change * 3500) / 30  # Surplus needed per day
                    tdee += calorie_surplus
                    print(
                        f"To gain {str(weight_gain_change)} pounds in a month, you need to consume {tdee:.2f} calories per day.")
                    break
            except ValueError:
                print("Please enter a valid number for weight gain.")

    elif goal == "lose":
        while True:
            try:
                weight_lose_change = float(input("How many pounds would you like to lose in a month? "))
                if weight_lose_change <= 0:
                    print("Loss must be a positive number.")
                else:
                    calorie_deficit = (weight_lose_change * 3500) / 30  # Deficit needed per day
                    tdee -= calorie_deficit
                    print(
                        f"To lose {str(weight_lose_change)} pounds in a month, you need to consume {tdee:.2f} calories per day.")
                    break
            except ValueError:
                print("Please enter a valid number for weight loss.")

    elif goal == "maintain":
        print(f"To maintain your weight, you need to consume {tdee:.2f} calories per day.")


    # Generate meal plan based on target calories
    meal_plan = generate_meal_plan(tdee)
    print("\nYour personalized meal plan:")
    print(meal_plan)

    # Generate workout plan based on goal and activity level
    workout_plan = generate_workout_plan(tdee, goal, activity_level)
    print("\nYour personalized workout plan:")
    print(workout_plan)


if __name__ == "__main__":
    main()
