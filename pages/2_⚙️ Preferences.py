import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from functions import show_session_state_sidebar
from functions import initialize_session_state

# ----------------------------------------------------------------------------------------------------

initialize_session_state()
#show_session_state_sidebar()

# ----------------------------------------------------------------------------------------------------
# Helper functions
options = ['Default', 'Somewhat important', 'Important', 'Very important', "Exclude"]
factors = {"Default": 1.0, "Somewhat important": 1.25, "Important": 1.5, "Very important": 2.0, "Exclude": 0.0}
macros_weight = st.session_state.profile['Weights']['Macros']
micros_weight = st.session_state.profile['Weights']['Micros']
nutrients_importance = st.session_state.profile['Importance']

def create_importance_radio(category, item):

    selected = st.radio(
        label=f"How important is {item} to you?",
        options=options, 
        index=options.index(st.session_state.profile['Importance'][f'{category}'][f'{item}']),
        horizontal=True,
        key=f'radio_{category}_{item}'
    )
    return selected

def set_default_nutritional_weights():
    default_macros_weight = {
    "Protein": 0.15,
    "Carbohydrates": 0.15,
    "Sugar": 0.10,
    "Fat": 0.15,
    "Saturated Fat": 0.05,
    "Trans Fat": 0.05,
    "Fiber": 0.05
    }

    default_micros_weights = {
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
    }

    for key, value in default_macros_weight.items():
        macros_weight[f'{key}'] = value

    for key, value in default_micros_weights.items():
        micros_weight[f'{key}'] = value
    

def adjust_weights_nutritional():
    set_default_nutritional_weights()
    adjusted_weights = {}
    total_sum = 0

    # Macro-nutrients
    for metric in macros_weight:
        adjusted_weights[f'Macros {metric}'] = macros_weight[metric] * factors.get(nutrients_importance['Macros'][metric])
        total_sum += adjusted_weights[f'Macros {metric}']
    
    for metric in micros_weight:
        adjusted_weights[f'Micros {metric}'] = micros_weight[metric] * factors.get(nutrients_importance['Micros'][f'{metric}'])
        total_sum += adjusted_weights[f'Micros {metric}']

    for item in adjusted_weights:
        item_list = item.split(" ", maxsplit=1)
        category = item_list[0]
        metric = item_list[1]
        if "Macros" in category:
            macros_weight[f'{metric}'] = adjusted_weights[f'{category} {metric}'] / total_sum
        else:
            micros_weight[f'{metric}'] = adjusted_weights[f'{category} {metric}'] / total_sum

def adjust_weights(category_name, normalized_sum):
    adjusted_weights = {}
    total_sum = 0

    for metric in st.session_state.profile['Weights'][category_name]:
        adjusted_weights[f'{metric}'] = st.session_state.profile['Weights'][category_name][metric] * factors.get(st.session_state.profile['Importance'][category_name][metric])
        total_sum += adjusted_weights[f'{metric}']

    for metric in st.session_state.profile['Weights'][category_name]:
        adjusted_weights[f'{metric}'] = (adjusted_weights[f'{metric}']/total_sum) * normalized_sum
    
    for metric in adjusted_weights:
        st.session_state.profile['Weights'][category_name][metric] = adjusted_weights[metric]
 
# ----------------------------------------------------------------------------------------------------
# Front-End
st.title("Enter your preferences")

st.markdown("The calculation is based on many different metrics and corresponding weights. Below you can find all the metrics that we take into account." \
" We provided a default value for each of these metrics, however, if you wish, you can change it by clicking how important certain metrics are." \
" You also have the choice to exclude a metric if that's what you want. Excluded metrics will not be considered in the calculation and ranking of the recipes, however, we will still provide information about them." \
" Exclude as many as you want, but leave at least one metric in each category (health, environment)!")

# Expanders for setting the weights

with st.expander("Overall Weights", expanded=False, icon="⚖️"):
    with st.form("overall_weights_form"):
        col1, col2, col3 = st.columns([1.5, 5, 1.5])  # adjust column ratios to suit layout

        with col1:
            st.markdown("⬅️ *Health*")

        with col2:
            importance = st.slider(
                "Select the importance",
                min_value=0,
                max_value=100,
                value=int(st.session_state.profile['Weights']['Overall']['Health']),
                step=1,
                label_visibility="collapsed"  # hide the built-in label to keep it clean
            )


        with col3:
            st.markdown("➡️ *Environment*")

        if st.form_submit_button("Save"):
            st.session_state.profile['Weights']['Overall']['Environment'] = importance
            st.session_state.profile['Weights']['Overall']['Health'] = 100 - st.session_state.profile['Weights']['Overall']['Environment']

            with st.spinner():
                    st.success("Changes saved!")
# ----------------------------------------------------------------------------------------------------
st.subheader("Health")
with st.expander("Macro-Nutrients", expanded=False, icon="📊"):

    with st.form("radio_macros_weights"):
        overall_preferences = {}

        for item in st.session_state.profile['Importance']['Macros']:
            st.write(f'{item}')
            selected = create_importance_radio('Macros', item)
            overall_preferences[f"{item}"] = selected

        if st.form_submit_button("Save"):
            for key in overall_preferences:
                st.session_state.profile['Importance']['Macros'][f'{key}'] = overall_preferences[key]

            adjust_weights_nutritional()

            with st.spinner():
                    st.success("Changes saved!")
        

# ----------------------------------------------------------------------------------------------------
with st.expander("Micro-Nutrients", expanded=False, icon="🥕"):

    with st.form("radio_micros_weights"):
        overall_preferences = {}

        for item in st.session_state.profile['Importance']['Micros']:
            st.write(f'{item}')
            selected = create_importance_radio('Micros', item)
            overall_preferences[f"{item}"] = selected

        if st.form_submit_button("Save"):
            for key in overall_preferences:
                st.session_state.profile['Importance']['Micros'][f'{key}'] = overall_preferences[key]

            adjust_weights_nutritional()

            with st.spinner():
                    st.success("Changes saved!")

# ----------------------------------------------------------------------------------------------------
st.subheader("Environment")
with st.expander("Environmental Aspects", expanded=False, icon="🌎"):
        
    with st.form("radio_environment_weights"):
        overall_preferences = {}

        for item in st.session_state.profile['Importance']['Environment']:
            st.write(f'{item}')
            selected = create_importance_radio('Environment', item)
            overall_preferences[f"{item}"] = selected

        if st.form_submit_button("Save"):
            for key in overall_preferences:
                st.session_state.profile['Importance']['Environment'][f'{key}'] = overall_preferences[key]

            adjust_weights('Environment', 1)

            with st.spinner():
                    st.success("Changes saved!")