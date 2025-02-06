from flask import Flask, render_template, request
import openai

# Set your OpenAI API key
openai.api_key = "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"

app = Flask(__name__)


# Function to convert pounds to kilograms
def poundstokg(body_weight):
    return body_weight * 0.453592


# Function to convert feet and inches to centimeters
def feetandinchestocm(feet, inches):
    return (feet * 30.48) + (inches * 2.54)


# BMR calculations for men and women
def bmrformen(kg, cm, age):
    return 10 * kg + 6.25 * cm - 5 * age + 5


def bmrforwomen(kg, cm, age):
    return 10 * kg + 6.25 * cm - 5 * age - 161


# Function to calculate BMI
def calculate_bmi(kg, cm):
    height_m = cm / 100
    return kg / (height_m ** 2)


# Generate meal plan using OpenAI
def generate_meal_plan(calories):
    prompt = f"Create a daily meal plan for {calories} calories. The plan should include breakfast, lunch, and dinner. Snacks can be added if needed. Please list the food items and the estimated calories for each meal."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use 'gpt-4' if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates personalized meal plans."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        meal_plan = response['choices'][0]['message']['content'].strip()
        return meal_plan
    except Exception as e:
        return f"Error generating meal plan: {str(e)}"


# Generate workout plan using OpenAI
def generate_workout_plan(calories, goal, activity_level):
    prompt = f"Create a personalized workout plan for someone who needs {calories} calories per day. The goal is to {goal}. Based on an activity level of {activity_level}, include exercises for chest, back, shoulders, biceps, triceps, and legs. Provide exercises, sets, reps, and time for each workout session."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use 'gpt-4' if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates personalized workout plans."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        workout_plan = response['choices'][0]['message']['content'].strip()
        return workout_plan
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        age = int(request.form["age"])
        sex = request.form["sex"]
        body_weight = float(request.form["body_weight"])
        feet = int(request.form["feet"])
        inches = int(request.form["inches"])
        goal = request.form["goal"]
        activity_level = request.form["activity_level"]

        # Convert weight and height
        kg = poundstokg(body_weight)
        cm = feetandinchestocm(feet, inches)

        # Calculate BMR
        if sex == "M":
            bmr = bmrformen(kg, cm, age)
        elif sex == "F":
            bmr = bmrforwomen(kg, cm, age)

        # Calculate TDEE based on activity level
        if activity_level == "1":
            tdee = bmr * 1.2
            activity_level_text = "Little to no exercise"
        elif activity_level == "2":
            tdee = bmr * 1.375
            activity_level_text = "Light exercise"
        elif activity_level == "3":
            tdee = bmr * 1.55
            activity_level_text = "Moderate exercise"
        elif activity_level == "4":
            tdee = bmr * 1.725
            activity_level_text = "Heavy exercise"
        elif activity_level == "5":
            tdee = bmr * 1.9
            activity_level_text = "Very heavy exercise"

        # Adjust TDEE based on goal (gain, lose, maintain)
        if goal == "gain":
            weight_change = float(request.form["weight_change"])
            calorie_surplus = (weight_change * 3500) / 30  # Surplus per day
            tdee += calorie_surplus
        elif goal == "lose":
            weight_change = float(request.form["weight_change"])
            calorie_deficit = (weight_change * 3500) / 30  # Deficit per day
            tdee -= calorie_deficit

        # Generate meal plan and workout plan
        meal_plan = generate_meal_plan(tdee)
        workout_plan = generate_workout_plan(tdee, goal, activity_level_text)

        return render_template("results.html", meal_plan=meal_plan, workout_plan=workout_plan, tdee=tdee)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
