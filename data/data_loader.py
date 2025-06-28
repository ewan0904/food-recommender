import pandas as pd
import streamlit as st
import ast

@st.cache_data
def load_micro_nutrient_reference_data():
    nutrient_df = pd.read_csv("ewan0904/food-recommender/data/datasets/micro-nutrients-reference.csv")
    return nutrient_df

@st.cache_data
def load_recipes_data():
    recipes_df = pd.read_excel("ewan0904/food-recommender/data/datasets/final_recipes.xlsx")
    recipes_df['Ingredients'] = recipes_df['Ingredients'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    recipes_df['Instructions'] = recipes_df['Instructions'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    return recipes_df

@st.cache_data
def load_ingredients_data():
    ingredients_df = pd.read_excel("ewan0904/food-recommender/data/datasets/final_ingredients.xlsx")
    return ingredients_df

