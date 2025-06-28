
import requests
import json
import streamlit as st

# The complete API endpoint URL for this flow
url = f"https://api.langflow.astra.datastax.com/lf/9e953ffc-8d4e-419e-bec2-1b07048aa540/api/v1/run/13f59e80-cd3e-4166-b7a8-a8514b8d2592"  

# Request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": st.secrets['Datastax_BEARER']  # Authentication key from environment variable'}
}


def get_recipe(input_value):
    # Request payload configuration
    payload = {
        "input_value": input_value,  # The input value to be processed by the flow
        "output_type": "text",  # Specifies the expected output format
        "input_type": "text",  # Specifies the input format
        "tweaks": {
            "AstraDB-0kWRk": {
                "number_of_results": 20
            } 
        }
    }

    try:
    # Send API request
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes

        response_text = response.json()['outputs'][0]['outputs'][0]['results']['text']['data']['text']
        
        # Print response
        recipe_ids = response_text.split(",")
        recipe_ids = [x.strip() for x in recipe_ids]
        return recipe_ids

    except requests.exceptions.RequestException as e:
        return f"Error making API request: {e}"
    except ValueError as e:
        return f"Error parsing response: {e}"
        