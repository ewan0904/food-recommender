import streamlit as st
from find_recipe import get_recipe
from data.data_loader import load_recipes_data, load_ingredients_data
import pandas as pd
from functions import show_session_state_sidebar
from functions import initialize_session_state
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import ast
import math
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# ----------------------------------------------------------------------------------------------------
st.markdown("# Find your Recipe")
initialize_session_state()
#show_session_state_sidebar()
# ----------------------------------------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------------------------------------
recipes_df = load_recipes_data()
ingredients_df = load_ingredients_data()
meals = st.session_state.profile['General']['Number_of_meals']
macros = st.session_state.profile['Macros']
micros = st.session_state.profile['Micros']
environment = st.session_state.profile['Environment']
weights = st.session_state.profile['Weights']

# ----------------------------------------------------------------------------------------------------
# Helper Functions - Calculations
# ----------------------------------------------------------------------------------------------------
# Macros
def calculate_macros_interval_score(name, value):
    weight = st.session_state.profile['Weights']['Macros'][name]
    lower_bound = (st.session_state.profile['Macros'][name][0]) / meals
    upper_bound = (st.session_state.profile['Macros'][name][1]) / meals
    interval = upper_bound - lower_bound

    # Check if the value is withing the interval, then it returns 1
    if lower_bound <= value <= upper_bound:
        return weight
    
    # Check if the value is below the lower bound of the interval
    elif lower_bound > value:
        return weight - min(weight, weight * ((lower_bound - value) / interval))
        
    else: 
        return weight - min(weight, weight * ((value - upper_bound) / interval))

# ----------------------------------------------------------------------------------------------------
def calculate_macros_UL_score(name, value):
    weight = st.session_state.profile['Weights']['Macros'][name]
    upper_limit = (st.session_state.profile['Macros'][name])/ meals

    if value <= upper_limit:
        return weight
    
    else:
        return weight - min(weight, weight * ((value - upper_limit) / upper_limit))

# ----------------------------------------------------------------------------------------------------
def calculate_macros_RDI_score(name, value):
    weight = st.session_state.profile['Weights']['Macros'][name]
    RDI = (st.session_state.profile['Macros'][name]) / meals

    if value == RDI:
        return weight

    else:
        deviation = abs((value - RDI) / RDI)
        return weight - min(weight, weight * deviation)

# ----------------------------------------------------------------------------------------------------
# Micros
def calculate_micros_UL_score(name, value):
    weight = st.session_state.profile['Weights']['Micros'][name]
    lower_bound = (st.session_state.profile['Micros'][name]) / meals # RDI
    upper_bound = (st.session_state.profile['Micros'][f'{name} UL']) / meals # Tolerable Upper Limit
    interval = upper_bound - lower_bound

    # Case 1: Value is within the optimal range → full score
    if lower_bound <= value <= upper_bound:
        return weight

    # Case 2: Value is below RDI → penalize based on how far below RDI (relative to RDI)
    elif value < lower_bound:
        deviation = (lower_bound - value) / lower_bound
        return weight - min(weight, weight * deviation)

    # Case 3: Value is above UL → penalize based on how far above UL (relative to interval)
    else:
        deviation = (value - upper_bound) / interval
        return weight - min(weight, weight * deviation)

# ----------------------------------------------------------------------------------------------------
def calculate_micros_RDI_score(name, value):
    weight = st.session_state.profile['Weights']['Micros'][name]
    RDI = (st.session_state.profile['Micros'][name]) / meals

    # Perfect match → full score
    if value == RDI:
        return weight

    # Calculate proportional deviation (absolute)
    deviation = abs(value - RDI) / RDI

    # Apply penalty
    return weight - min(weight, weight * deviation)

# ----------------------------------------------------------------------------------------------------
# Environment
def calculate_environment_score(name, value):
    weight = st.session_state.profile['Weights']['Environment'][name]
    threshold = (st.session_state.profile['Environment'][name]) / meals

    if value <= threshold:
        return weight
    
    else:
        return weight - min(weight, weight * ((value - threshold) / threshold))

# ----------------------------------------------------------------------------------------------------
# Total score
def calculate_score(recipe_id):
    health_contributions = {}
    environmental_contributions = {}
    recipe = recipes_df[recipes_df['recipe_id'] == recipe_id].iloc[0]

    # Macros - Interval
    health_contributions['Protein'] = calculate_macros_interval_score('Protein', recipe['protein'])
    health_contributions['Fat'] = calculate_macros_interval_score('Fat', recipe['fat'])
    health_contributions['Carbohydrates'] = calculate_macros_interval_score('Carbohydrates', recipe['carbs'])
    # Macros - UL
    health_contributions['Saturated Fat'] = calculate_macros_UL_score('Saturated Fat', recipe['saturates'])
    health_contributions['Trans Fat'] = calculate_macros_UL_score('Trans Fat', recipe['Trans Fat (g)'])
    health_contributions['Sugar'] = calculate_macros_UL_score('Sugar', recipe['sugars'])
    # Macros - RDI
    health_contributions['Fiber'] = calculate_macros_RDI_score('Fiber', recipe['fibre'])
    # Micros - UL
    health_contributions['Calcium'] = calculate_micros_UL_score('Calcium', recipe['Calcium (mg)'])
    health_contributions['Iodine'] = calculate_micros_UL_score('Iodine', recipe['Iodine (µg)'])
    health_contributions['Iron'] = calculate_micros_UL_score('Iron', recipe['Iron (mg)'])
    health_contributions['Selenium'] = calculate_micros_UL_score('Selenium', recipe['Selenium (µg)'])
    health_contributions['Zinc'] = calculate_micros_UL_score('Zinc', recipe['Zinc (mg)'])
    health_contributions['Vitamin A'] = calculate_micros_UL_score('Vitamin A', recipe['Vitamin A RE (µg)'])
    health_contributions['Vitamin D'] = calculate_micros_UL_score('Vitamin D', recipe['Vitamin D (µg)'])
    health_contributions['Vitamin E'] = calculate_micros_UL_score('Vitamin E', recipe['Vitamin E (mg)'])
    # Micros - RDI
    health_contributions['Magnesium'] = calculate_micros_RDI_score('Magnesium', recipe['Magnesium (mg)'])
    health_contributions['Salt'] = calculate_micros_RDI_score('Salt', recipe['salt'])
    health_contributions['Vitamin B1'] = calculate_micros_RDI_score('Vitamin B1', recipe['Vitamin B1 (mg)'])
    health_contributions['Vitamin B2'] = calculate_micros_RDI_score('Vitamin B2', recipe['Vitamin B2 (mg)'])
    health_contributions['Vitamin B3'] = calculate_micros_RDI_score('Vitamin B3', recipe['Vitamin B3 (mg)'])
    health_contributions['Vitamin B6'] = calculate_micros_RDI_score('Vitamin B6', recipe['Vitamin B6 (mg)'])
    health_contributions['Vitamin B9'] = calculate_micros_RDI_score('Vitamin B9', recipe['Vitamin B9 (µg)'])
    health_contributions['Vitamin B12'] = calculate_micros_RDI_score('Vitamin B12', recipe['Vitamin B12 (µg)'])
    health_contributions['Vitamin C'] = calculate_micros_RDI_score('Vitamin C', recipe['Vitamin C (mg)'])
    health_contributions['Vitamin K'] = calculate_micros_RDI_score('Vitamin K', recipe['Vitamin K (µg)'])
    # Environment
    environmental_contributions['Climate Change'] = calculate_environment_score('Climate Change', recipe['Total - Co2 eq'])
    environmental_contributions['Ozone Layer Depletion'] = calculate_environment_score('Ozone Layer Depletion', recipe['Total - CFC11 eq'])
    environmental_contributions['Particulate Matter'] = calculate_environment_score('Particulate Matter', recipe['Total - disease inc.'])
    environmental_contributions['Toxicological Effects'] = calculate_environment_score('Toxicological Effects', recipe['Total - NC CTUh'])
    environmental_contributions['Toxicological Effects (carcinogenic)'] = calculate_environment_score('Toxicological Effects (carcinogenic)', recipe['Total - C CTUh'])
    environmental_contributions['Acidification'] = calculate_environment_score('Acidification', recipe['Total - mol H+ eq'])
    environmental_contributions['Freshwater Eutrophication'] = calculate_environment_score('Freshwater Eutrophication', recipe['Total - P eq'])
    environmental_contributions['Marine Eutrophication'] = calculate_environment_score('Marine Eutrophication', recipe['Total - N eq'])
    environmental_contributions['Land Use'] = calculate_environment_score('Land Use', recipe['Total - pt dimensionless'])
    environmental_contributions['Water Use'] = calculate_environment_score('Water Use', recipe['Total - m3'])
    environmental_contributions['Energy Use'] = calculate_environment_score('Energy Use', recipe['Total - MJ'])
    return health_contributions, environmental_contributions

# ----------------------------------------------------------------------------------------------------
# Helper Functions - HTML/Warning
# ----------------------------------------------------------------------------------------------------
def render_bar_macros_interval(name, unit, value, lower, upper):
    try:
        value = float(value)
        lower = float(lower) / meals
        upper = float(upper) / meals
        target_str = f"{lower:.1f}–{upper:.1f} {unit}"
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return
    
    # Color logic
    if value < lower:
        color = "#FFA500"  # orange
    elif value > upper:
        color = "#FF4136"  # red
    else:
        color = "#2ECC71"  # green

    # Determine max scale
    max_value = max(value, upper) * 1.2 if upper else value * 1.5

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    interval_start = (lower / max_value) * 100
    interval_width = ((upper - lower) / max_value) * 100 if upper != lower else 0

    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
            <span>{name}</span>
            <span>Actual: {value:.1f} g &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: {target_str}</span>
        </div>
        <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
            position: absolute;
            left: {interval_start:.1f}%;
            width: {interval_width:.1f}%;
            top: 0;
            bottom: 0;
            background-color: rgba(0, 120, 0, 0.5);
            border-radius: 6px;
            z-index: 1;">
        </div>

    </div>
    """
    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_macros_UL(name, unit, value, upper):
    try:
        value = float(value)
        upper = float(upper) / meals
        target_str = f"{upper:.1f} {unit}"
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return
    
    # Color logic
    if value <= upper:
        color = "#2ECC71"  # orange
    else:
        color = "#FF4136"  # red

    # Determine max scale
    max_value = max(value, upper) * 1.2 if upper else value * 1.5

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    upper_percent = min(upper/max_value, 1.0) * 100

    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
            <span>{name}</span>
            <span>Actual: {value:.1f} g &nbsp;&nbsp;|&nbsp;&nbsp; Limit: {target_str}</span>
        </div>
        <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
            <div style="
                position: absolute;
                left: {upper_percent:.1f}%;
                top: 0;
                bottom: 0;
                width: 5px;
                background-color: #FF4136;
                z-index: 2;">
            </div>
    </div>
    """
    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_macros_RDI(name, unit, value, RDI):
    try:
        value = float(value)
        RDI = float(RDI) / meals
        target_str = f"{RDI:.1f} {unit}"
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return
    
    # Target range ±15%
    lower = RDI * 0.85
    upper = RDI * 1.15

    # Color logic
    if value < RDI:
        color = "#FFA500"  # orange
    elif value > RDI:
        color = "#FF4136"  # red
    elif value > lower & value < upper:
        color = "#2ECC71" # green
    else:
        color = "#2ECC71"  # green

    # Determine max scale
    max_value = max(value, RDI) * 1.2 if RDI else value * 1.5

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    interval_start = (lower / max_value) * 100
    interval_width = ((upper - lower) / max_value) * 100 if upper != lower else 0
    RDI_percent = min(RDI/max_value, 1.0) * 100

    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
            <span>{name}</span>
            <span>Actual: {value:.1f} g &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: {target_str}</span>
        </div>
        <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
            <div style="
                position: absolute;
                left: {interval_start:.1f}%;
                width: {interval_width:.1f}%;
                top: 0;
                bottom: 0;
                background-color: rgba(0, 120, 0, 0.5);
                border-radius: 6px;
                z-index: 1;">
            </div>
    </div>
    """
    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_micros_RDI(name, unit, value, RDI):
    try:
        value = float(value)
        RDI = float(RDI) / meals
        target_str = f"{RDI:.1f} {unit}"
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return
    
    # Target range ±15%
    lower = RDI * 0.85
    upper = RDI * 1.15

    # Color logic
    if value < lower:
        color = "#FFA500"  # orange
    elif value > upper:
        color = "#FFA500"  # red
    else:
        color = "#2ECC71"  # green

    # Determine max scale
    max_value = max(value, upper) * 1.2

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    interval_start = (lower / max_value) * 100
    interval_width = ((upper - lower) / max_value) * 100 if upper != lower else 0
    RDI_percent = min(RDI/max_value, 1.0) * 100

    # Render bar
    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
        <span>{name}</span>
        <span>Actual: {value:.1f} {unit} &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: {target_str}</span>
    </div>

    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
            position: absolute;
            left: {interval_start:.1f}%;
            width: {interval_width:.1f}%;
            top: 0;
            bottom: 0;
            background-color: rgba(0, 120, 0, 0.5);
            border-radius: 6px;
            z-index: 1;">
        </div>
    </div>
    """

    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_micros_RDI_UL(name, unit, value, RDI, UL):
    try:
        value = float(value)
        RDI = float(RDI) / meals
        UL = float(UL) / meals
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return
    
    # Target range ±15%
    lower = RDI * 0.85
    upper = RDI * 1.15

    # Color logic
    if value < lower:
        color = "#FFA500"  # orange
    elif value > UL:
        color = "#FF4136"  # red
    elif value > upper:
        color = "#FFA500"  # orange
    else:
        color = "#2ECC71"  # green

    # Determine max scale
    max_value = max(value, upper) * 1.2

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    interval_start = (lower / max_value) * 100
    interval_width = ((upper - lower) / max_value) * 100 if upper != lower else 0
    RDI_percent = min(RDI/max_value, 1.0) * 100
    limit_percent = min(UL/max_value, 1.0) * 100

    # Render bar
    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
        <span>{name}</span>
        <span>Actual: {value:.1f} {unit} &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: {RDI:.1f} {unit} &nbsp;&nbsp;|&nbsp;&nbsp; Limit: {UL:.1f} {unit}</span>
    </div>

    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
            position: absolute;
            left: {interval_start:.1f}%;
            width: {interval_width:.1f}%;
            top: 0;
            bottom: 0;
            background-color: rgba(0, 120, 0, 0.5);
            border-radius: 6px;
            z-index: 1;">
        </div>
        <div style="
                position: absolute;
                left: {limit_percent:.1f}%;
                top: 0;
                bottom: 0;
                width: 5px;
                background-color: red;
                z-index: 2;">
        </div>

    </div>
    """

    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_micros_UL(name, unit, value, UL):
    try:
        value = float(value)
        UL = float(UL) / meals
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return

    # Color logic
    if value > UL:
        color = "#FF4136"  # red
    else:
        color = "#2ECC71"  # green

    # Determine max scale
    max_value = max(value, UL) * 1.2

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    limit_percent = min(UL/max_value, 1.0) * 100

    # Render bar
    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
        <span>{name}</span>
        <span>Actual: {value:.1f} {unit} &nbsp;&nbsp;|&nbsp;&nbsp; Limit: {UL:.1f} {unit}</span>
    </div>

    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
                position: absolute;
                left: {limit_percent:.1f}%;
                top: 0;
                bottom: 0;
                width: 5px;
                background-color: #FF4136;
                z-index: 2;">
        </div>
    </div>
    """

    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def blend_hex(c1, c2, t: float) -> str:
    """
    Linear-interpolate between two hex colours.
    c1, c2  – strings like '#RRGGBB'
    t       – 0 → return c1, 1 → return c2
    """
    c1 = c1.lstrip('#'); c2 = c2.lstrip('#')
    r1, g1, b1 = tuple(int(c1[i : i+2], 16) for i in (0, 2, 4))
    r2, g2, b2 = tuple(int(c2[i : i+2], 16) for i in (0, 2, 4))
    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)
    return f"#{r:02X}{g:02X}{b:02X}"

# ----------------------------------------------------------------------------------------------------
def render_bar_environment(name, unit, value, threshold, multiplier, decimal):
    try:
        value = float(value) * multiplier
        threshold = (float(threshold)) / meals
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return

    # Color logic
    SAFE_COLOUR   = "#2ECC71"   # deep green
    ALERT_COLOUR  = "#FFA500"   # orange
    DANGER_COLOUR = "#FF4136"   # red

    ratio = value / threshold

    if value >= threshold:
        # ❶ Above the upper limit → solid red
        color = DANGER_COLOUR
    elif ratio < 0:
        # ❷ Below the limit – blend green→orange as value→UL
        #    ratio = 0   (value = 0)      -> SAFE_COLOUR (green)
        #    ratio = 1   (value = UL-ε)   -> ALERT_COLOUR (orange)
        color = SAFE_COLOUR
        # optional easing to make colour change faster near the limit
    else:
        ratio = math.pow(ratio, 1.5)            # tweak γ here if you like
        color = blend_hex(SAFE_COLOUR, ALERT_COLOUR, ratio)

    # Determine max scale
    max_value = max(value, threshold) * 1.2

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    limit_percent = min(threshold/max_value, 1.0) * 100

    # Render bar
    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
        <span>{name}</span>
        <span>Actual: {value:.{decimal}f} {unit} &nbsp;&nbsp;|&nbsp;&nbsp; Threshold: {threshold:.{decimal}f} {unit}</span>
    </div>

    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
                position: absolute;
                left: {limit_percent:.{decimal}f}%;
                top: 0;
                bottom: 0;
                width: 5px;
                background-color: #FF4136;
                z-index: 2;">
        </div>
    </div>
    """

    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_environment_median(name, unit, value, threshold, multiplier, decimal):
    try:
        value = float(value) * multiplier
        threshold = (float(threshold)) * multiplier
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return

    # Color logic
    SAFE_COLOUR   = "#2ECC71"   # deep green
    ALERT_COLOUR  = "#FFA500"   # orange
    DANGER_COLOUR = "#FF4136"   # red

    ratio = value / threshold

    if value >= threshold:
        # ❶ Above the upper limit → solid red
        color = DANGER_COLOUR
    elif ratio < 0:
        # ❷ Below the limit – blend green→orange as value→UL
        #    ratio = 0   (value = 0)      -> SAFE_COLOUR (green)
        #    ratio = 1   (value = UL-ε)   -> ALERT_COLOUR (orange)
        color = SAFE_COLOUR
        # optional easing to make colour change faster near the limit
    else:
        ratio = math.pow(ratio, 1.5)            # tweak γ here if you like
        color = blend_hex(SAFE_COLOUR, ALERT_COLOUR, ratio)

    # Determine max scale
    max_value = max(value, threshold) * 1.2

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    limit_percent = min(threshold/max_value, 1.0) * 100

    # Render bar
    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
        <span>{name}</span>
        <span>Actual: {value:.{decimal}f} {unit} &nbsp;&nbsp;|&nbsp;&nbsp; Median: {threshold:.{decimal}f} {unit}</span>
    </div>

    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
                position: absolute;
                left: {limit_percent:.{decimal}f}%;
                top: 0;
                bottom: 0;
                width: 5px;
                background-color: #FF4136;
                z-index: 2;">
        </div>
    </div>
    """

    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_bar_human_health(name, value, threshold, divider):
    try:
        value = (1 / float(value)) / divider
        threshold = float(threshold) /divider
    except (ValueError, TypeError):
        st.warning(f"{name} value is not numeric")
        return

    # Color logic
    SAFE_COLOUR   = "#2ECC71"   # deep green
    ALERT_COLOUR  = "#FFA500"   # orange
    DANGER_COLOUR = "#FF4136"   # red

    if value <= threshold:
        # ❶ Above the upper limit → solid red
        color = DANGER_COLOUR
    else:
        ratio = math.pow((threshold / value), 1.5)
        color = blend_hex(SAFE_COLOUR, ALERT_COLOUR, ratio)

    # Determine max scale
    max_value = max((value), threshold) * 1.2

    # Percent widths
    value_percent = min(value / max_value, 1.0) * 100
    limit_percent = min(threshold/max_value, 1.0) * 100

    # Render bar
    bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
        <span>{name}</span>
        <span>Acutal: 1 in {value:.2f} million &nbsp;&nbsp;|&nbsp;&nbsp; Median: 1 in {threshold:.2f} million</span>
    </div>

    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
        <div style="width: {value_percent:.1f}%; background-color: {color}; height: 100%;"></div>
        <div style="
                position: absolute;
                left: {limit_percent:.1f}%;
                top: 0;
                bottom: 0;
                width: 5px;
                background-color: #FF4136;
                z-index: 2;">
        </div>
    </div>
    """
    st.markdown(bar, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------
def render_warning_environmental(value, description, recipe_id):
    if value == 0:
        st.success(f"✅ All ingredients were able to be backed up by {description} data!")
    else:
        missing_codes = ingredients_df[(ingredients_df['recipe_id'] == recipe_id) & (ingredients_df['Agribalyse Code'].isna())]
        missing_codes['quantity'] = missing_codes['quantity'].fillna('')
        missing_ingredients_list = (missing_codes['quantity'].str.strip() + ' ' + missing_codes['ingredient'].str.strip()).str.strip().tolist()
        formatted_list = '\n- ' + '\n -'.join(missing_ingredients_list)
        st.warning(f"""🟠 {value} ingredients could not be backed up by {description} data. The {description} rating could slightly vary from the actual rating!\nMissing data on: {formatted_list}""")

# ----------------------------------------------------------------------------------------------------
def render_warning_nutritional(value, description, recipe_id):
    if value == 0:
        st.success(f"✅ All ingredients were able to be backed up by {description} data!")
    else:
        missing_codes = ingredients_df[(ingredients_df['recipe_id'] == recipe_id) & (ingredients_df['NEVO Code'].isna())]
        missing_codes['quantity'] = missing_codes['quantity'].fillna('')
        missing_ingredients_list = (missing_codes['quantity'].str.strip() + ' ' + missing_codes['ingredient'].str.strip()).str.strip().tolist()
        formatted_list = '\n' + '\n'.join(f"- {item}" for item in missing_ingredients_list)
        st.warning(f"""🟠 {value} ingredients could not be backed up by {description} data. The {description} rating regarding the **vitamins and minerals** could slightly vary from the actual rating!\nMissing data on: {formatted_list}""")

# ----------------------------------------------------------------------------------------------------
# Beginning of the UI
# ----------------------------------------------------------------------------------------------------

def recipe_tab(input_value):
    allergies_intolerances = f"""Please exclude any recipes containing ingredients I'm allergic or intolerant to.
    Allergies & Intolerances: {st.session_state.profile['General']['Allergies_Intolerances']}, 
    Make sure the recipes are completely free from these, including hidden or derivative ingredients."""

    prompt = f"{input_value}. {allergies_intolerances}"

    recipe_ids = get_recipe(prompt)
    recipe_ids_int = []
    for rid in recipe_ids:
        try:
            recipe_ids_int.append(int(rid))
        except ValueError:
            pass  # or log/collect invalid ones if needed
    results = []
    filtered_recipes = recipes_df[recipes_df['recipe_id'].isin(recipe_ids_int)]
    # Iterate over all recipes
    for _, recipe_row in filtered_recipes.iterrows():
        recipe_id = recipe_row['recipe_id']
        rating = float(recipe_row['Rating'])
        title = recipe_row['Title']  # Make sure 'title' matches your actual column name

        try:
            # Calculate scores
            health_contributions, environmental_contributions = calculate_score(recipe_id)

            health_weight = st.session_state.profile['Weights']['Overall']['Health']
            environment_weight = st.session_state.profile['Weights']['Overall']['Environment']

            health_score = (sum(health_contributions.values()) * 100)
            environment_score = (sum(environmental_contributions.values()) * 100)
            final_score = (health_weight / 100) * health_score + (environment_weight / 100) * environment_score

            # Append result
            results.append({
                'recipe_id': recipe_id,
                'title': title,
                'rating': rating,
                'health_score': health_score,
                'environment_score': environment_score,
                'final_score': final_score
            })

        except Exception as e:
            st.warning(f"Skipping recipe {recipe_id} due to error: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(results)
    df[['health_score', 'environment_score', 'final_score']] = df[['health_score', 'environment_score', 'final_score']]

    st.session_state.profile['other']['recipe_df'] = df

# ----------------------------------------------------------------------------------------------------
# Find Recipe Form
# ----------------------------------------------------------------------------------------------------
with st.form("find_recipe_form"):

    recipe_description = st.text_input("Recipe Description", help="The more details you provide, the better results you will get." \
    "You can include ingredients, specific values for macro-nutrients (e.g. more than 10g of protein), a specific cuisine, or even how long it takes to make." \
    "E.g. 'Show me a recipe containing chicken, with at least 15g of protein and from the Asian cuisine.'")

    find_recipe_form_submit = st.form_submit_button("Find Recipe")
    if find_recipe_form_submit:
        if not recipe_description.strip():
            st.error("Please enter a recipe description")
        else:
            recipe_tab(recipe_description)

# ----------------------------------------------------------------------------------------------------
# # Grid options
# ----------------------------------------------------------------------------------------------------
recipe_df = st.session_state.profile['other']['recipe_df']
if recipe_df is not None:
    st.info("""
            The table below shows you a collection of different recipes that matched with your prompt. 
            You can click on any of them to get more details.

            The user rating represents real users' feedback, ranging from 1 star (worst) to 5 star (best).

            The other ratings show how well a recipe is performing when looking at its nutritional composition related to human health, environmental impact, and a combined score. 
            All of the ratings are calculated based on your preferences, and range from 0 (worst) to 100 (best).
            """,  icon="ℹ️")
    
    gb = GridOptionsBuilder.from_dataframe(recipe_df)
    gb.configure_selection('single', use_checkbox=False)  # Single cell selection
    gb.configure_grid_options(domLayout="normal")
    gb.configure_pagination(enabled=True, paginationPageSize=5)
    gb.configure_column("final_score", sort='desc')
    # Set widths for specific columns
    gb.configure_column("recipe_id", header_name="ID", width=70)
    gb.configure_column("title", header_name="Title", width=250)
    gb.configure_column("rating", header_name="User\nRating", width=80, headerTooltip="Actual user ratings, from 1 (worst) to 5 (best)")
    gb.configure_column("health_score", valueFormatter="value.toFixed(0)", header_name="Health\nRating", width=120, headerTooltip="Nutritional rating, from 0 (worst) to 100 (best)")
    gb.configure_column("environment_score", valueFormatter="value.toFixed(0)", header_name="Environment\nRating", width=140, headerTooltip="Environmental rating, from 0 (worst) to 100 (best)")
    gb.configure_column("final_score", valueFormatter="value.toFixed(0)", header_name="Overall\nRating", width=120, headerTooltip="Combined rating (nutritional & environmental), from 0 (worst) to 100 (best)")
    grid_options = gb.build()

    grid_response = AgGrid(
        recipe_df,
        gridOptions=grid_options,
        theme= 'streamlit',
        update_mode='SELECTION_CHANGED',
        enable_enterprise_modules=False,
        fit_columns_on_grid_load=True,
        reload_data=True,
        allow_unsafe_jscode=True
        )

    # Check if a row is selected
    selected_rows = grid_response['selected_rows']

    if selected_rows is not None and not selected_rows.empty:
        recipe_id = selected_rows['recipe_id'].values[0]
        selected_recipe = recipes_df[recipes_df['recipe_id'] == recipe_id].iloc[0]
        recipe_tab, nutrition_tab, environment_tab = st.tabs(['**🥘 Recipe**', '**🥗 Nutrition**', '**🌳 Environment**'])

# ----------------------------------------------------------------------------------------------------
# Recipe Tab
# ----------------------------------------------------------------------------------------------------
        with recipe_tab:
            image_url = selected_recipe['Image_url']
            recipe_name = selected_recipe['Title']
            serves = selected_recipe['Servings']
            difficulty = selected_recipe['Difficulty']
            prep_time = selected_recipe['Prep_time']
            cook_time = selected_recipe['Cook_time']
            recipe_url = selected_recipe['Url']
            ingredients = selected_recipe['Ingredients']
            instructions = selected_recipe['Instructions']
            rating = selected_recipe['Rating']
            rating_percentage = (rating / 5) * 100
            number_of_ratings = selected_recipe['Number_of_ratings']

# ----------------------------------------------------------------------------------------------------
            # Build HTML
            html_content = f"""
            <div style="text-align: center;">
                <h1 style="margin-bottom: 0;">{recipe_name}</h1>
                    <div style="display:inline-block; position: relative; font-size: 24px; line-height: 1;">
                    <div style="color: lightgray;">★★★★★</div>
                    <div style="position: absolute; top: 0; left: 0; overflow: hidden; width: {rating_percentage}%; color: gold;">★★★★★</div>
                        <span style="font-size: 16px; color: #555;">(Out of {number_of_ratings} ratings)</span>
                    </div>
                <p style="margin-bottom: 8px;">
                    <a href="{recipe_url}" target="_blank" style="text-decoration: none; font-size: 14px; color: #1f77b4;">
                        View full recipe on BBC Good Food
                    </a>
                </p>

                <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 10px 0 20px 0;">
                    <div style="border: 1px solid black; border-radius: 8px; padding: 8px 12px;">Serves {serves}</div>
                    <div style="border: 1px solid black; border-radius: 8px; padding: 8px 12px;">{difficulty}</div>
                    <div style="border: 1px solid black; border-radius: 8px; padding: 8px 12px;"><strong>Prep:</strong> {prep_time}</div>
                    <div style="border: 1px solid black; border-radius: 8px; padding: 8px 12px;"><strong>Cook:</strong> {cook_time}</div>
                </div>

                <img src="{image_url}" alt="no image found" width="400" style="border-radius: 15px;" />
            </div>
            """

            # ✅ Render with full HTML support
            components.html(html_content, height=500)
# ----------------------------------------------------------------------------------------------------

            ingredients_tab, instructions_tabs = st.columns([1, 1.5])  # image left, info right

            with ingredients_tab:

                def render_ingredients(items):
                    lines = [
                        f'<li>{item["quantity"]} {item["ingredient"]}</li>'
                        for item in items
                    ]
                    html = "<ul style='margin:0 0 0 1.2em; padding:0; line-height:1.6;'>{}</ul>".format("".join(lines))
                    st.markdown(html, unsafe_allow_html=True)

                st.markdown("### 📝 Ingredients")
                render_ingredients(ingredients)

            with instructions_tabs:
                # Flatten and sort the steps
                sorted_steps = sorted(
                    [(int(list(step.keys())[0]), list(step.values())[0]) for step in instructions],
                    key=lambda x: x[0]
                )

                # Title
                st.markdown("### 🧑‍🍳 Instructions")

                # Display steps with numbering
                for num, text in sorted_steps:
                    st.markdown(f"**Step {num}**  \n{text}")

# ----------------------------------------------------------------------------------------------------
# Nutrition Tab
# ----------------------------------------------------------------------------------------------------
        with nutrition_tab:

            with st.expander("📊 **How to read the bar charts?**"):
                st.markdown("""
                <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                        <span>Example 1</span>
                        <span>Actual: 70g &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: 60-80g</span>
                    </div>
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden;">
                    <div style="width: 70%; background-color: #2ECC71; height: 100%;"></div>
                    <div style="
                        position: absolute;
                        left: 60%;
                        width: 20%;
                        top: 0;
                        bottom: 0;
                        background-color: rgba(0, 120, 0, 0.5);
                        border-radius: 6px;
                        z-index: 1;">
                    </div>
            
                </div>
                            
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value lies within the recommended range and it is considered healthy.*""")
                st.markdown("""
            
                <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                        <span>Example 2</span>
                        <span>Actual: 40g &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: 60-80g</span>
                    </div>
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden;">
                    <div style="width: 40%; background-color: #FFA500; height: 100%;"></div>
                    <div style="
                        position: absolute;
                        left: 60%;
                        width: 20%;
                        top: 0;
                        bottom: 0;
                        background-color: rgba(0, 120, 0, 0.5);
                        border-radius: 6px;
                        z-index: 1;">
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value falls short and can indicate a minor or major insufficiency.*""")
                st.markdown("""
            
                <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                        <span>Example 3</span>
                        <span>Actual: 90g &nbsp;&nbsp;|&nbsp;&nbsp; Recommended: 60-80g</span>
                    </div>
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden;">
                    <div style="width: 90%; background-color: #FF4136; height: 100%;"></div>
                    <div style="
                        position: absolute;
                        left: 60%;
                        width: 20%;
                        top: 0;
                        bottom: 0;
                        background-color: rgba(0, 120, 0, 0.5);
                        border-radius: 6px;
                        z-index: 1;">
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value exceeds the recommended range and can potentially cause problems.*""")
                st.markdown("""
                <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                    <span>Example 4</span>
                    <span>Actual: 4g &nbsp;&nbsp;|&nbsp;&nbsp; Limit: 8g</span>
                </div>
            
                <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
                    <div style="width: 40%; background-color: #2ECC71; height: 100%;"></div>
                    <div style="
                            position: absolute;
                            left: 80%;
                            top: 0;
                            bottom: 0;
                            width: 5px;
                            background-color: #FF4136;
                            z-index: 2;">
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value is below the limit and it is considered good.*""")
            
            with st.expander("**🔥 Calories**"):
                kcal_per_day = int(st.session_state.profile['Macros']['Calories'])
                kcal_per_meal = int(kcal_per_day / meals)
                kcal_recipe = int(selected_recipe['kcal'])
                st.markdown(f"""
                <div style='font-family: "Source Sans Pro", sans-serif; font-size: 1rem;'>
                Based on your personal information, your advised caloric intake per day is <b>{kcal_per_day} kcal</b>. \n
                And since you prefer to have {meals} meals per day, the caloric intake per meal is <b>{kcal_per_meal} kcal</b>.\n
                This recipe contains <b>{kcal_recipe} kcal</b> per serving.
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🥦 **Macro-Nutrients**"):
                render_bar_macros_interval("Protein", "g", selected_recipe['protein'], macros['Protein'][0], macros['Protein'][1])
                render_bar_macros_interval("Carbohydrates", "g", selected_recipe['carbs'], macros['Carbohydrates'][0], macros['Carbohydrates'][1])
                render_bar_macros_UL("Sugar", "g", selected_recipe['sugars'], macros['Sugar'])
                render_bar_macros_interval("Fat", "g", selected_recipe['fat'], macros['Fat'][0], macros['Fat'][1])
                render_bar_macros_UL("Saturated Fat", "g", selected_recipe['saturates'], macros['Saturated Fat'])
                render_bar_macros_UL("Trans Fat", "g", selected_recipe['Trans Fat (g)'], macros['Trans Fat'])
                render_bar_macros_RDI("Fiber", "g", selected_recipe['fibre'], macros['Fiber'])

            with st.expander("🍊 **Vitamins**"):
                render_bar_micros_RDI_UL("Vitamin A", "µg", selected_recipe['Vitamin A RE (µg)'], micros['Vitamin A'], micros['Vitamin A UL'])
                render_bar_micros_RDI("Vitamin B1", "g", selected_recipe['Vitamin B1 (mg)'], micros['Vitamin B1'])
                render_bar_micros_RDI("Vitamin B2", "g", selected_recipe['Vitamin B2 (mg)'], micros['Vitamin B2'])
                render_bar_micros_RDI("Vitamin B3", "g", selected_recipe['Vitamin B3 (mg)'], micros['Vitamin B3'])
                render_bar_micros_RDI("Vitamin B6", "g", selected_recipe['Vitamin B6 (mg)'], micros['Vitamin B6'])
                render_bar_micros_RDI("Vitamin B9", "µg", selected_recipe['Vitamin B9 (µg)'], micros['Vitamin B9'])
                render_bar_micros_RDI("Vitamin B12", "µg", selected_recipe['Vitamin B12 (µg)'], micros['Vitamin B12'])
                render_bar_micros_RDI("Vitamin C", "mg", selected_recipe['Vitamin C (mg)'], micros['Vitamin C'])
                render_bar_micros_RDI_UL("Vitamin D", "µg", selected_recipe['Vitamin D (µg)'], micros['Vitamin D'], micros['Vitamin D UL'])
                render_bar_micros_RDI_UL("Vitamin E", "mg", selected_recipe['Vitamin E (mg)'], micros['Vitamin E'], micros['Vitamin E UL'])
                render_bar_micros_RDI("Vitamin K", "µg", selected_recipe['Vitamin K (µg)'], micros['Vitamin K'])

            with st.expander("🧂 **Minerals**"):
                render_bar_micros_UL("Salt", "g", selected_recipe['salt'], micros['Salt'])
                render_bar_micros_RDI_UL("Calcium", "mg", selected_recipe['Calcium (mg)'], micros['Calcium'], micros['Calcium UL'])
                render_bar_micros_RDI_UL("Iodine", "mg", selected_recipe['Iodine (µg)'], micros['Iodine'], micros['Iodine UL'])
                render_bar_micros_RDI_UL("Iron", "mg", selected_recipe['Iron (mg)'], micros['Iron'], micros['Iron UL'])
                render_bar_micros_RDI("Magnesium", 'mg', selected_recipe['Magnesium (mg)'], micros['Magnesium'])
                render_bar_micros_RDI_UL("Selenium", "µg", selected_recipe['Selenium (µg)'], micros['Selenium'], micros['Selenium UL'])
                render_bar_micros_RDI_UL("Zinc", "mg", selected_recipe['Zinc (mg)'], micros['Zinc'], micros['Zinc UL'])
            st.markdown("---")
            render_warning_nutritional(selected_recipe['number_of_ingredients'] - selected_recipe['number_of_nevo_codes'], "nutritional", recipe_id)
# ----------------------------------------------------------------------------------------------------
# Environment Tab
# ----------------------------------------------------------------------------------------------------
        with environment_tab:

            with st.expander("📊 **How to read the bar charts?**"):
                st.markdown("""
                    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                            <span>Example 5</span>
                            <span>Actual: 2kg &nbsp;&nbsp;|&nbsp;&nbsp; Threshold: 5kg</span>
                        </div>
            
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
                        <div style="width: 20%; background-color: #64C254; height: 100%;"></div>
                        <div style="
                                position: absolute;
                                left: 50%;
                                top: 0;
                                bottom: 0;
                                width: 5px;
                                background-color: #FF4136;
                                z-index: 2;">
                        </div>
                    </div>
                    
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value is below the threshold and is considered safe.*""")
                st.markdown("""
                    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                            <span>Example 6</span>
                            <span>Actual: 7kg &nbsp;&nbsp;|&nbsp;&nbsp; Threshold: 5kg</span>
                        </div>
            
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
                        <div style="width: 70%; background-color: #FF4136; height: 100%;"></div>
                        <div style="
                                position: absolute;
                                left: 50%;
                                top: 0;
                                bottom: 0;
                                width: 5px;
                                background-color: #FF4136;
                                z-index: 2;">
                        </div>
                    </div>
                    
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value exceeds the threshold and is considered unsafe.*""")
                st.markdown("""
                    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                            <span>Example 7</span>
                            <span>Actual: 1 in 2 million &nbsp;&nbsp;|&nbsp;&nbsp; Median: 1 in 4 million</span>
                        </div>
            
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
                        <div style="width: 20%; background-color: #FF4136; height: 100%;"></div>
                        <div style="
                                position: absolute;
                                left: 40%;
                                top: 0;
                                bottom: 0;
                                width: 5px;
                                background-color: #FF4136;
                                z-index: 2;">
                        </div>
                    </div>
                    
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value represents a fraction and is therefore higher than the median, which is considered relatively bad. It means that the consumption of a recipe compared to the median value of all recipes causes more cases of illnesses. (Read more under Human-Health Metrics above)*""")
                st.markdown("""
                    <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px;">
                            <span>Example 8</span>
                            <span>Actual: 1 in 4 million &nbsp;&nbsp;|&nbsp;&nbsp; Median: 1 in 2 million</span>
                        </div>
            
                    <div style="position: relative; height: 14px; background-color: #eee; border-radius: 7px; overflow: hidden; margin-bottom: 12px;">
                        <div style="width: 40%; background-color: #2ECC71; height: 100%;"></div>
                        <div style="
                                position: absolute;
                                left: 20%;
                                top: 0;
                                bottom: 0;
                                width: 5px;
                                background-color: #FF4136;
                                z-index: 2;">
                        </div>
                    </div>
                    
                """, unsafe_allow_html=True)
                st.markdown("""> *The actual value represents a fraction and is therefore lower than the median, which is considered relatively good. It means that the consumption of a recipe compared to the median value of all recipes causes less cases of illnesses. (Read more under Human-Health Metrics above)*""")


            
            with st.expander("**🟢 Categories with safe thresholds**"):
                render_bar_environment("Acification", "mol H+", selected_recipe['Total - mol H+ eq'], environment['Acidification'], 1, 3)
                render_bar_environment("Climate Change", "kg CO₂", selected_recipe['Total - Co2 eq'], environment['Climate Change'], 1, 2)
                render_bar_environment("Energy Use", "MJ", selected_recipe['Total - MJ'], environment['Energy Use'], 1, 1)
                render_bar_environment("Freshwater Eutrophication", "g Phospherus", selected_recipe['Total - P eq'], environment['Freshwater Eutrophication'], 1000, 1)
                render_bar_environment("Marine Eutrophication", "g Nitrogen", selected_recipe['Total - N eq'], environment['Marine Eutrophication'], 1000, 2)
                render_bar_environment("Ozone Layer Depletion", "µg CFC-11", selected_recipe['Total - CFC11 eq'], environment['Ozone Layer Depletion'], 1000000000, 2)
                render_bar_environment("Water Use", "m³", selected_recipe['Total - m3'], environment['Water Use'], 1, 2)
            
            with st.expander("**📊 Categories compared with median values**"):
                render_bar_environment_median("Land Use", "", selected_recipe['Total - pt dimensionless'], environment['Land Use'], 1, 1)
                render_bar_human_health("Particulate Matter", selected_recipe['Total - disease inc.'], environment['Particulate Matter'], 1000000)
                render_bar_human_health("Toxicological Effects", selected_recipe['Total - NC CTUh'], environment['Toxicological Effects'], 1000000)
                render_bar_human_health("Toxicological Effects (carcinogenic)", selected_recipe['Total - C CTUh'], environment['Toxicological Effects (carcinogenic)'], 1000000)               

            st.markdown("---")
            render_warning_environmental(selected_recipe['number_of_ingredients'] - selected_recipe['number_of_agribalyse_codes'], "environmental", recipe_id)

elif st.session_state.profile['other']['recipe_df'] is None:
    st.write("")
else:
    st.warning("Unfortunately, no recipes were found that fitted the recipe description. Please try again by altering the prompt. You could extend the description with more information, or try to search for another recipe.")
