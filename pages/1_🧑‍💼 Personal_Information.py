import streamlit as st
import pandas as pd
from data.data_loader import load_micro_nutrient_reference_data
from functions import initialize_session_state, show_session_state_sidebar
from auth import check_auth

check_auth()  # 🔐 Protect this page

# ----------------------------------------------------------------------------------------------------

nutrient_df = load_micro_nutrient_reference_data()

# ----------------------------------------------------------------------------------------------------
# Sidebar
initialize_session_state()
#show_session_state_sidebar()

# ----------------------------------------------------------------------------------------------------

# FRONTEND
# Set page config
st.markdown("# Personal Information")
st.write("""
    In order to provide you with the best food recommendations, we need some personal information. Please fill out the form below.
         """)

@st.fragment()
def personal_data_form():
    with st.form("personal_data_form"):
        st.header("Personal Data")

        name = st.text_input("Name *", value=st.session_state.profile["General"]["Name"])
        age = st.number_input("Age *", min_value=19, max_value=120, step=1, value=st.session_state.profile["General"]["Age"])
        genders = ["Male", "Female"]
        gender = st.radio("Gender *", genders, index=genders.index(st.session_state.profile["General"]["Gender"]))
        weight = st.number_input(
            "Weight (kg) *",
            min_value=0.0,
            max_value=300.0,
            step=0.1,
            value=st.session_state.profile["General"]["Weight"],
            format="%.1f",
        )
        height = st.number_input(
            "Height (cm) *",
            min_value=0.0,
            max_value=220.0,
            step=1.0,
            value=st.session_state.profile["General"]["Height"],
            format="%.0f",
        )
        activities = (
            "Sedentary: little or no exercise",
            "Light: exercise 1-3 times/week",
            "Moderate: exercise 3-5 times/week",
            "Active: daily exercise or intense exercise 3-4 times/week",
            "Very active: intense exercise 6-7 times/week"
        )
        activity_level = st.selectbox("Activity Level *", activities, index=activities.index(st.session_state.profile["General"]["Activity_level"]))
        allergies_intolerances = st.text_input("Allergies & Intolerances", value=st.session_state.profile["General"]['Allergies_Intolerances'], help="E.g. nuts, seafood, lactose")
        number_of_meals = st.number_input("Preferred Number of Meals *", min_value=1, max_value=10, step=1, value=st.session_state.profile["General"]["Number_of_meals"])

        personal_data_form_submit = st.form_submit_button("Save")
        if personal_data_form_submit:
            if all([name, age, gender, weight, height, activity_level]):
                st.session_state.profile["General"]["Name"] = name
                st.session_state.profile["General"]["Age"] = age
                st.session_state.profile["General"]["Gender"] = gender
                st.session_state.profile["General"]["Weight"] = weight
                st.session_state.profile["General"]["Height"] = height
                st.session_state.profile["General"]["Activity_level"] = activity_level
                st.session_state.profile["General"]["Allergies_Intolerances"] = allergies_intolerances
                st.session_state.profile["General"]["Number_of_meals"] = number_of_meals

                # Determine the Macros
                Macros = calculate_Macros(
                    weight=weight,
                    height=height,
                    age=age,
                    gender=gender,
                    activity_level=activity_level,
                )
                st.session_state.profile["Macros"]["Calories"] = Macros["calories"]
                st.session_state.profile["Macros"]["Protein"] = Macros["Macros"]["protein"]
                st.session_state.profile["Macros"]["Carbohydrates"] = Macros["Macros"]["carbs"]
                st.session_state.profile["Macros"]["Sugar"] = Macros["Macros"]["sugar"]
                st.session_state.profile["Macros"]["Fat"] = Macros["Macros"]["fat"]
                st.session_state.profile["Macros"]["Saturated Fat"] = Macros["Macros"]["saturated_fat"]
                st.session_state.profile["Macros"]["Trans Fat"] = Macros["Macros"]["trans_fat"]

                # Determine the Micros
                Micros = get_micronutrient_targets(age=age, gender=gender, df=nutrient_df)
                st.session_state.profile["Micros"]["Calcium"] = Micros["Calcium (mg)"]
                st.session_state.profile["Micros"]["Calcium UL"] = Micros["Calcium UL (mg)"]
                st.session_state.profile["Micros"]["Iodine"] = Micros["Iodine (µg)"]
                st.session_state.profile["Micros"]["Iodine UL"] = Micros["Iodine UL (µg)"]
                st.session_state.profile["Micros"]["Iron"] = Micros["Iron (mg)"]
                st.session_state.profile["Micros"]["Iron UL"] = Micros["Iron UL (mg)"]
                st.session_state.profile["Micros"]["Magnesium"] = Micros["Magnesium (mg)"]
                st.session_state.profile["Micros"]["Selenium"] = Micros["Selenium (µg)"]
                st.session_state.profile["Micros"]["Selenium UL"] = Micros["Selenium UL (µg)"]
                st.session_state.profile["Micros"]["Salt"] = Micros["Salt (g)"]
                st.session_state.profile["Micros"]["Zinc"] = Micros["Zinc (mg)"]
                st.session_state.profile["Micros"]["Zinc UL"] = Micros["Zinc UL (mg)"]
                st.session_state.profile["Micros"]["Vitamin A"] = Micros["Vitamin A RE (µg)"]
                st.session_state.profile["Micros"]["Vitamin A UL"] = Micros["Vitamin A RE UL (µg)"]
                st.session_state.profile["Micros"]["Vitamin B1"] = Micros["Vitamin B1 (mg)"]
                st.session_state.profile["Micros"]["Vitamin B2"] = Micros["Vitamin B2 (mg)"]
                st.session_state.profile["Micros"]["Vitamin B3"] = Micros["Vitamin B3 (mg)"]
                st.session_state.profile["Micros"]["Vitamin B6"] = Micros["Vitamin B6 (mg)"]
                st.session_state.profile["Micros"]["Vitamin B9"] = Micros["Vitamin B9 (µg)"]
                st.session_state.profile["Micros"]["Vitamin B12"] = Micros["Vitamin B12 (µg)"]
                st.session_state.profile["Micros"]["Vitamin C"] = Micros["Vitamin C (mg)"]
                st.session_state.profile["Micros"]["Vitamin D"] = Micros["Vitamin D (µg)"]
                st.session_state.profile["Micros"]["Vitamin D UL"] = Micros["Vitamin D UL (µg)"]
                st.session_state.profile["Micros"]["Vitamin E"] = Micros["Vitamin E (mg)"]
                st.session_state.profile["Micros"]["Vitamin E UL"] = Micros["Vitamin E UL (mg)"]
                st.session_state.profile["Micros"]["Vitamin K"] = Micros["Vitamin K (µg)"]
                st.session_state.profile["Macros"]["Fiber"] = Micros["Fiber (g)"]

                with st.spinner():
                    st.success("Personal data saved!")
            else:
                st.warning("Please fill in all required (*) fields.")

 
# ----------------------------------------------------------------------------------------------------
# Functionality

# Function to calculate the daily caloric intake
def calculate_Macros(weight, height, age, gender, activity_level):
    """
    Calculate daily caloric intake based on TDEE using Mifflin-St Jeor Equation.
    """
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factors = {
        "Sedentary: little or no exercise": 1.2,
        "Light: exercise 1-3 times/week": 1.375,
        "Moderate: exercise 3-5 times/week": 1.55,
        "Active: daily exercise or intense exercise 3-4 times/week": 1.725,
        "Very active: intense exercise 6-7 times/week": 1.9,
    }

    factor = activity_factors.get(activity_level, 1.2)
    tdee = bmr * factor

    Macros_kcal = {
        "protein": (0.10 * tdee, 0.15 * tdee),
        "carbs": (0.45 * tdee, 0.65 * tdee),
        "sugar": (0.10 * tdee, 0.10 * tdee),  # fixed %
        "fat": (0.20 * tdee, 0.35 * tdee),
        "saturated_fat": (0.10 * tdee, 0.10 * tdee),  # fixed %
        "trans_fat": (0.01 * tdee, 0.01 * tdee),  # fixed %
    }

    # Convert kcal to grams
    Macros_grams = {
        "protein": (
            int(Macros_kcal["protein"][0] / 4),
            int(Macros_kcal["protein"][1] / 4),
        ),
        "carbs": (int(Macros_kcal["carbs"][0] / 4),
                  int(Macros_kcal["carbs"][1] / 4)),
        "sugar": (int(Macros_kcal["sugar"][0] / 4)),
        "fat": (int(Macros_kcal["fat"][0] / 9),
                int(Macros_kcal["fat"][1] / 9)),
        "saturated_fat": (int(Macros_kcal["saturated_fat"][0] / 9)),
        "trans_fat": (int(Macros_kcal["trans_fat"][0] / 9)),
    }

    return {"calories": round(tdee, 0), "Macros": Macros_grams}


# Function to match the micro-nutrient
def get_micronutrient_targets(age, gender, df):
    # Normalize input
    gender = gender.lower()

    # Convert gender to match CSV
    gender = "female" if gender == "female" else "male"

    # Find matching age group
    def age_in_range(age_str):
        if "+" in age_str:
            return age > int(age_str.replace("+", ""))
        start, end = map(int, age_str.split("-"))
        return start <= age <= end

    # Filter DataFrame
    match = df[(df["Gender"].str.lower() == gender) & (df["Age"].apply(age_in_range))]

    if match.empty:
        return None  # Or raise an error

    # Convert to dict (drop Gender and Age columns)
    row = match.iloc[0].drop(["Gender", "Age"]).to_dict()
    # Optionally round all numeric values
    row = {k: round(v, 1) for k, v in row.items()}

    return row


def forms():
    personal_data_form()


# ----------------------------------------------------------------------------------------------------
# Initialize application
if __name__ == "__main__":
    forms()
