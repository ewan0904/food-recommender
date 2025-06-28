import streamlit as st

# Initializing and styling functions
def initialize_session_state():
    if "profile" not in st.session_state:
            st.session_state.profile = {
                "General": {
                    "Name": "",
                    "Age": 25,
                    "Gender": "Male",
                    "Weight": 70.0,
                    "Height": 175.0,
                    "Activity_level": "Sedentary: little or no exercise",
                    "Allergies_Intolerances": "",
                    "Number_of_meals": 3
                },
                "Macros": {
                    "Calories": 0.0,
                    "Protein": 0.0,
                    "Carbohydrates": 0.0,
                    "Sugar": 0.0,
                    "Fat": 0.0,
                    "Saturated Fat": 0.0,
                    "Trans Fat": 0.0,
                    "Fiber": 0.0
                },
                "Micros": {
                    "Calcium": 0.0,
                    "Calcium UL": 0.0,
                    "Iodine": 0.0,
                    "Iodine UL": 0.0,
                    "Iron": 0.0,
                    "Iron UL": 0.0,
                    "Magnesium": 0.0,
                    "Selenium": 0.0,
                    "Selenium UL": 0.0,
                    "Salt": 0.0,
                    "Zinc": 0.0,
                    "Zinc UL": 0.0,
                    "Vitamin A": 0.0,
                    "Vitamin A UL": 0.0,
                    "Vitamin B1": 0.0,
                    "Vitamin B2": 0.0,
                    "Vitamin B3": 0.0,
                    "Vitamin B6": 0.0,
                    "Vitamin B9": 0.0,
                    "Vitamin B12": 0.0,
                    "Vitamin C": 0.0,
                    "Vitamin D": 0.0,
                    "Vitamin D UL": 0.0,
                    "Vitamin E": 0.0,
                    "Vitamin E UL": 0.0,
                    "Vitamin K": 0.0
                },
                "Environment": {
                  "Climate Change": 891/365, # kg CO2-eq, 2.7t CO2 * 0.33 * 1000
                  "Ozone Layer Depletion": 19, # µg CFC-11-eq
                  "Acidification": 100/365, # mol H+
                  "Water Use": 0.5, # m3
                  "Energy Use": 35, # MJ
                  # Median
                #   "Freshwater Eutrophication": 0.0004029, # kg P
                  "Freshwater Eutrophication": 3.3, # g P
                  "Marine Eutrophication": 18.7, # g N
                  "Land Use": 340.28, # dimensionless - took the median value
                # 1 in a {number}
                  "Particulate Matter": 1/2.10187441762859e-07, # disease inc.
                  "Toxicological Effects": 1/4.613457745796e-08, # CTUh
                  "Toxicological Effects (carcinogenic)": 1/2.177513927337e-09 # CTUh
                },
                "Weights": {
                    "Overall": {
                    "Health": 50.0,
                    "Environment": 50.0,   
                     },
                    "Macros": {
                    "Protein": 0.15,
                    "Carbohydrates": 0.15,
                    "Sugar": 0.10,
                    "Fat": 0.15,
                    "Saturated Fat": 0.05, 
                    "Trans Fat": 0.05,
                    "Fiber": 0.05,    
                     },
                    "Micros": {
                    "Calcium": 1/60,
                    "Iodine": 1/60,
                    "Iron": 1/60,
                    "Magnesium": 1/60,
                    "Selenium": 1/60,
                    "Salt": 1/60,
                    "Zinc": 1/60,
                    "Vitamin A": 1/60,
                    "Vitamin B1": 1/60,
                    "Vitamin B2": 1/60,
                    "Vitamin B3": 1/60,
                    "Vitamin B6": 1/60,
                    "Vitamin B9": 1/60,
                    "Vitamin B12": 1/60,
                    "Vitamin C": 1/60,
                    "Vitamin D": 1/60,
                    "Vitamin E": 1/60,
                    "Vitamin K": 1/60
                    },
                    "Environment": {
                        "Climate Change": 1/11,
                        "Ozone Layer Depletion": 1/11,
                        "Particulate Matter": 1/11,
                        "Toxicological Effects": 1/11,
                        "Toxicological Effects (carcinogenic)": 1/11,
                        "Acidification": 1/11,
                        "Freshwater Eutrophication": 1/11,
                        "Marine Eutrophication": 1/11,
                        "Land Use": 1/11,
                        "Water Use": 1/11,
                        "Energy Use": 1/11
                    }
                },
                "Importance": {
                    "Overall": {
                    "Health": "Default",
                    "Environment": "Default",   
                     },
                    "Macros": {
                    "Protein": "Default",
                    "Carbohydrates": "Default",
                    "Sugar": "Default",
                    "Fat": "Default",
                    "Saturated Fat": "Default", 
                    "Trans Fat": "Default",
                    "Fiber": "Default",    
                     },
                    "Micros": {
                    "Calcium": "Default",
                    "Iodine": "Default",
                    "Iron": "Default",
                    "Magnesium": "Default",
                    "Selenium": "Default",
                    "Salt": "Default",
                    "Zinc": "Default",
                    "Vitamin A": "Default",
                    "Vitamin B1": "Default",
                    "Vitamin B2": "Default",
                    "Vitamin B3": "Default",
                    "Vitamin B6": "Default",
                    "Vitamin B9": "Default",
                    "Vitamin B12": "Default",
                    "Vitamin C": "Default",
                    "Vitamin D": "Default",
                    "Vitamin E": "Default",
                    "Vitamin K": "Default"
                    },
                    "Environment": {
                        "Climate Change": "Default",
                        "Ozone Layer Depletion": "Default",
                        "Particulate Matter": "Default",
                        "Toxicological Effects": "Default",
                        "Toxicological Effects (carcinogenic)": "Default",
                        "Acidification": "Default",
                        "Freshwater Eutrophication": "Default",
                        "Marine Eutrophication": "Default",
                        "Land Use": "Default",
                        "Water Use": "Default",
                        "Energy Use": "Default"
                    }
                },
                "other": {
                    "session_sidebar_checkbox": False,
                    "recipe_df": None
                 }
        } 

def show_session_state_sidebar():
    # Use checkbox with stored value
    show_session_state = st.sidebar.checkbox(
        "Show Session State",
        value=st.session_state.get("show_session_state_checkbox"),
        key="show_session_state_checkbox"
    )

    # Update the session state with current value
    st.session_state.profile["other"]["session_sidebar_checkbox"] = show_session_state

    # Display session state if checkbox is checked
    if show_session_state:
        with st.sidebar.expander("Session State Details", expanded=True):
            st.sidebar.json(dict(st.session_state))


