import streamlit as st

st.title("More Information")

st.header("🌱 Environmental Metrics")

# --------------------------------------------------
# 1. Climate Change
# --------------------------------------------------
with st.expander("🌍 **Climate Change (kg CO₂-equivalents)**"):
    st.markdown(
        """
        **What is it?**  
        The amount of greenhouse gases (GHGs) a recipe is responsible for – mainly **CO₂, methane,**  
        and **nitrous oxide** – all rolled into one number that tells us how much the meal warms the planet.

        **How do we measure it?**  
        Every gas is converted into the warming power of CO₂ and added up, so we get a single value in  
        **kilograms of CO₂-equivalents (kg CO₂-eq)** per recipe.

        **Why does it matter for food?**  
        - Agriculture makes up ~33 % of global GHGs, which represents a significant influence to global warming.  
        - Seeing the number of a recipe helps us understand how much CO₂-equivalents are likely emitted and rank the recipes appropriately.

        **Threshold**  
        - A safe operating threshold is about **2.44 kg of CO₂-equivalents** per day.
        - This threshold represents a daily carbon budget per person. If everyone in the world kept their emissions within this limit, 
        it would keep total global carbon emissions within the remaining carbon budget — helping to limit global warming to no more than **2°C**, 
        as agreed under the Paris Agreement.
        """
    )

# --------------------------------------------------
# 2. Ozone-Layer Depletion
# --------------------------------------------------
with st.expander("🌀 **Ozone-Layer Depletion (kg CFC-11-equivalents)**"):
    st.markdown(
        """
        **What is it?**  
        A score showing how much a recipe’s supply chain could thin the ozone layer – the Earth’s sunscreen  
        that blocks harmful UV radiation.

        **How do we measure it?**  
        We express all ozone-eating chemicals (old fridges, certain crop-cooling agents, etc.) as  
        **kilograms of CFC-11-equivalents (kg CFC-11-eq)**.

        **Why does it matter for food?**  
        - Modern farming uses refrigerated storage and some specialty chemicals.  
        - Leaks or outdated coolants can still hurt the ozone layer.  

        **Threshold**  
        - An estimated safe threshold for food-related ozone layer depletion is about **19 µg CFC-11-equivalents** per day per capita.
        - Even though food systems only make up a small contribution to the global ozone layer depletion process, food choices can further reduce it.
        """
    )

# --------------------------------------------------
# 3. Acidification
# --------------------------------------------------
with st.expander("🌧️ **Acidification (mol H⁺-equivalents)**"):
    st.markdown(
        """
        **What is it?**  
        The potential of a recipe to create **acid rain** or acidify soils and freshwater. Big culprits are  
        **ammonia** from manure and **SO₂ / NOₓ** from fuel burning.

        **How do we measure it?**  
        All acid-forming emissions are expressed as **moles of hydrogen ions (mol H⁺-eq)** – the more H⁺,  
        the more acidic.

        **Why does it matter for food?**  
        - Acid rain damages crops, forests, and fish habitats.  

        **Threshold**  
        - **0.27 mol H⁺-equivalents** per day per capita
        """
    )

# --------------------------------------------------
# 4. Freshwater Eutrophication
# --------------------------------------------------
with st.expander("🏞️ **Freshwater Eutrophication (g P-equivalents)**"):
    st.markdown(
        """
        **What is it?**  
        Phospherus is a chemical compound that is commonly found in agricultural fertilizers. The problem arises when extra **phosphorus** get into rivers & lakes, causing algae blooms and fish dead zones.

        **How do we measure it?**  
        Everything is summed up as **grams of phosphorus equivalents (g P-eq)** per serving.

        **Why does it matter for food?**  
        - Manure and run-off from fertilised fields are top phosphorus sources.  
        - Lower-P recipes help keep freshwater ecosystems clear and oxygen-rich.

        **Threshold**
        - **3.3 g of P-equivalents per day per capita**
        """
    )

# --------------------------------------------------
# 5. Marine Eutrophication
# --------------------------------------------------
with st.expander("🌊 **Marine Eutrophication (g N-equivalents)**"):
    st.markdown(
        """
        **What is it?**  
        Similarly to Phospherus, nitrogen is a chemical compound that is commonly used as agricultural fertilizers. Nitogen run-off (mainly **nitrate** and **ammonium**) that flows to seas and creates coastal “dead zones.”

        **How do we measure it?**  
        Expressed as **grams of nitrogen equivalents (g N-eq)** per serving.

        **Why does it matter for food?**  
        - Intensive livestock and fertiliser use drive nitrogen pollution.  
        - Tracking N-impact guides us toward diets that protect oceans.

        **Threshold**  
        - **18.7 g N-equivalents per day per capita**
        """
    )

# --------------------------------------------------
# 6. Land Use
# --------------------------------------------------
with st.expander("🌾 **Land Use (dimensionless, point system)**"):
    st.markdown(
        """
        **What is it?**  
        Land use reflects how much land is occupied - and for how long — to produce the ingredients in a food item. 
        It includes the space used for growing crops, grazing animals, and any changes made to the land (like deforestation for pasture).

        **How do we measure it?**  
        Land use impact is translated into a dimensionless score in "pt" (points).
        These points express the relative environmental damage from land use (e.g. impacts on biodiversity, soil quality, and ecosystem services).
        The higher the points, the greater the environmental impact associated with land use - indicating more pressure on ecosystems, biodiversity, and natural resources.

        **Why does it matter for food?**  
        - More land use can mean deforestation and habitat loss.  
        - Helps us spot recipes that spare forests and wildlife corridors.

        **Median**  
        - Instead of a fixed threshold, we use the median value considering the land use impacts of all recipes.
        - The median value is **340.28 pt**.
        """
    )
    
# --------------------------------------------------
# 7. Water Use
# --------------------------------------------------
with st.expander("🚿 **Water Use (m³)**"):
    st.markdown(
        """
        **What is it?**  
        All freshwater consumed - irrigation, cleaning, processing - summed for one serving.

        **How do we measure it?**  
        Shown in **cubic metres (m³)** of water per recipe.

        **Why does it matter for food?**  
        - Agriculture is ~70 % of global freshwater withdrawals.
        - Animal feed and thirsty crops (e.g., almonds, rice) drive water footprints up.  

        **Threshold**  
        - **0.5 m³ of water** per day per capita 
        """
    )

# --------------------------------------------------
# 8. Energy Use
# --------------------------------------------------
with st.expander("**⚡ Energy Use (MJ)**"):
    st.markdown(
        """
        **What is it?**  
        The total energy needed to farm, process, transport, refrigerate, and cook the meal.

        **How do we measure it?**  
        Calculated in **megajoules (MJ)** per recipe, covering primary energy sources.

        **Why does it matter for food?**  
        - Higher usage of primary energy sources also drives up CO₂-emissions, which is harmful for the climate.
        - Primary energy resources are finite and an efficient usage is important for sustainability and long-term energy security.
        - Highlights recipes that are more energy efficient (think raw salads vs. slow-roasted meat).

        **Rule-of-thumb threshold**  
        - **35 MJ** per day per capita
        """
    )

st.header("🩺 Human-Health Metrics")

# --------------------------------------------------
# 1. Particulate-Matter Health Impact
# --------------------------------------------------
with st.expander("🌫️ **Particulate Matter - increase in disease cases**"):
    st.markdown(
        """
        **What is it?**  
        Tiny airborne particles (PM₂.₅ and PM₁₀) that get into our lungs and bloodstream, \
        raising the risk of **asthma, heart attacks, and strokes**.

        **How do we measure it?**  
        Life-cycle models account for various sources of particulate matter (PM) emissions—including those from field machinery, transport, 
        energy production, and even household cooking. These emissions are then linked to their estimated impact on human health, based on how much pollution is generated throughout the product's life cycle.

        **Median**  
        - We use the median value across all recipes as reference incidence rate. For this category it is about **2.10187441762859e-07**.
        - The very small number stands for the expected cases of illness for a recipe.
        - After some transformation, we get 1 / 2.10187441762859e-07 ≈ 4.76 million. So, if a recipe with this small value would be made 4.76 million times, it would cause 1 case of illness.
        """
    )

# --------------------------------------------------
# 2. Toxicological Effects – Non-Carcinogenic
# --------------------------------------------------
with st.expander("🧪 **Toxicological Effects (non-cancer) - NC CTUh**"):
    st.markdown(
        """
        **What is it?**  
        The chance that chemicals in the food chain cause **non-cancer health problems** \
        such as neuro-developmental issues, hormonal disruption, or organ toxicity.

        **How do we measure it?**  
        All relevant emissions (pesticides, processing chemicals, packaging additives) are \
        normalised to **Non-Cancer Comparative Toxic Units for Humans (NC CTUh)**.  
        One CTUh ≈ one extra case of disease over a million people exposed.

        **Why does it matter for food?**  
        - **Pesticide drift** can affect farm workers and nearby residents.  
        - Some additives or cleaning agents can enter waterways and come back in our diets.  
        - Flagging high NC CTUh recipes encourages safer farming and processing practices.

        **Median**  
        - We use the median value across all recipes as reference incidence rate. For this category it is about **4.613457745796e-08**.
        - The very small number stands for the expected cases of illness for a recipe.
        - After some transformation, we get 1 / 4.613457745796e-08 ≈ 21.67 million. So, if a recipe with this small value would be made 21.67 million times, it would cause 1 case of illness.
        """
    )

# --------------------------------------------------
# 3. Toxicological Effects – Carcinogenic
# --------------------------------------------------
with st.expander("☠️ **Toxicological Effects (cancer) - CTUh**"):
    st.markdown(
        """
        **What is it?**  
        The long-term potential of chemicals released along the recipe's supply chain to \
        **cause cancer** in humans.

        **How do we measure it?**  
        The same toxic inventory is converted to **Carcinogenic Comparative Toxic Units \
        for Humans (CTUh)**.  
        CTUh maps exposure to an expected fraction of additional cancer cases.

        **Median**  
        - We use the median value across all recipes as reference incidence rate. For this category it is about **2.177513927337e-09**.
        - The very small number stands for the expected cases of illness for a recipe.
        - After some transformation, we get 1 / 2.177513927337e-09 ≈ 459 million. So, if a recipe with this small value would be made 459 million times, it would cause 1 case of illness.
        """
    )

# --- Nutritional Metrics Section ---
with st.expander("🍎 **Nutritional Metrics**"):
    st.markdown("""For very interested users, we would recommend to have a look on the [National Institute of Health website](https://ods.od.nih.gov/HealthInformation/healthinformation.aspx).
                You can find more detailed information on the various professional health fact sheets. The information below only shows what the specific nutrients are useful or essential for.
                The recommended daily intakes and limits of nutrients can also be found on the website.""")

    st.subheader("Macronutrients")
    st.markdown("**Protein**  \nVital for muscle repair and immune function. Too little causes muscle loss; too much may stress kidneys.")
    st.markdown("**Carbohydrates**  \nMain energy source. Low intake causes fatigue; excess (especially refined) contributes to obesity and diabetes.")
    st.markdown("**Sugar**  \nToo much sugar contributes to obesity, tooth decay, and metabolic disease.")
    st.markdown("**Fat**  \nNecessary for hormones and energy. Too much can lead to obesity and heart disease.")
    st.markdown("**Saturated Fat**  \nLinked to increased LDL cholesterol and heart disease when consumed in excess.")
    st.markdown("**Trans Fat**  \nArtificial fats with strong links to cardiovascular disease. Should be minimized or avoided.")
    st.markdown("**Salt**  \nNecessary for fluid balance. Too much raises blood pressure and stroke risk.")
    st.markdown("**Fibre**  \nSupports digestion, stabilizes blood sugar, and reduces cholesterol.")

    st.subheader("Micronutrients")
    micronutrients = {
        "Calcium": "Crucial for strong bones and muscle function. Deficiency causes bone weakness.",
        "Iodine": "Supports thyroid hormone production. Lack can lead to goitre and cognitive issues.",
        "Iron": "Needed for red blood cell production. Deficiency leads to anemia and fatigue.",
        "Magnesium": "Aids in muscle/nerve function. Low intake may lead to cramps and heart issues.",
        "Selenium": "Functions as an antioxidant. Both too little and too much are harmful.",
        "Zinc": "Essential for immunity and healing. Deficiency impairs growth and immune response.",
        "Vitamin A": "Supports vision and immunity. Too little leads to blindness; too much can be toxic.",
        "Vitamin B1 (Thiamine)": "Needed for energy metabolism. Deficiency causes nerve and heart disorders.",
        "Vitamin B2 (Riboflavin)": "Helps with energy and skin health. Deficiency affects skin and eyes.",
        "Vitamin B3 (Niacin)": "Crucial for metabolism. Deficiency causes pellagra; excess may harm the liver.",
        "Vitamin B6": "Important for metabolism and brain function. Imbalance can cause nerve issues.",
        "Vitamin B9 (Folate)": "Supports DNA synthesis and pregnancy. Low levels risk birth defects.",
        "Vitamin B12": "Vital for nerve and blood cell health. Deficiency can cause anemia and nerve damage.",
        "Vitamin C": "Boosts immunity and antioxidant defense. Deficiency causes scurvy.",
        "Vitamin D": "Helps absorb calcium. Deficiency can lead to rickets and weak bones.",
        "Vitamin E": "Protects cells from oxidative damage. Rare deficiencies can affect nerves.",
        "Vitamin K": "Essential for blood clotting and bone strength. Deficiency causes bleeding issues."
    }

    for name, text in micronutrients.items():
        st.markdown(f"**{name}**  \n{text}")

# --------------------------------------------------
# Other useful information
# --------------------------------------------------
st.header("📦 Other")
with st.expander("🔢 **Calculation**"):
    st.write('')

    st.markdown("""
                ### 🩺 Health Scoring System

                In this system, each recipe is assessed using **25 nutritional metrics**:
                - **7 macronutrients** (e.g. protein, fat, carbs)
                - **7 minerals** (e.g. calcium, iron, zinc)
                - **11 vitamins** (e.g. vitamin A, D, B12)

                Each of these nutrients is given a **weight** to indicate how important it is in the overall health score.

                ---

                #### ⚙️ How Nutritional Scoring Works

                - **Each nutrient's score** is based on how closely the amount in the recipe aligns with recommended daily intake values.
                - Some nutrients also have **upper limits** – if a recipe exceeds those, the score drops accordingly.
                - If a recipe’s value is **far from the recommended range**, it will negatively affect the score.
                - But — each nutrient only affects the score **as much as its weight allows**.

                For example:  
                If you give **calcium** a low weight, even if a recipe has too much or too little, it won’t drag the overall score down much. But if you give it high importance, it has more influence.

                > *Note: The recommended daily intake and limits are divided by the number of preferred meals.*

                ---

                ### 🌍 Environmental Scoring System

                Environmental metrics evaluate the **ecological impact** of recipes, using standardized indicators (e.g. CO₂ emissions, land use, water use).

                Each environmental metric has a:
                - **Threshold** (a benchmark for acceptable impact)
                - Or a **median value** used for comparison

                The closer a recipe stays **within these bounds**, the better its environmental score.  
                The more a recipe **exceeds** these limits, the worse it performs.

                As with nutritional scoring:
                - The **weight** you assign to each metric controls how much it affects the final score.
                - Even if a recipe is very high in CO₂ or land use, its effect on the total score depends on **how much weight** you’ve given that metric.

                > *Note: The thresholds and median values are divided by the number of preferred meals.*

                ---

                ### ⚖️ Final Score

                The final score you see is a **combination of the health and environmental scores**.

                You can adjust the balance in the **Preferences**:

                - **Default**: 50% health, 50% environment
                - You can shift this toward **just health**, **just environment**, or anywhere in between.

                **Final Score = (Health Score × Health Weight) + (Environmental Score × Environmental Weight)**  

                ---

                #### 🧠 Weighting System

                You can set how important each metric is to **you** in the **Preferences** section.  
                Each metric has a default weight, and your selections apply multipliers based on the following scale:

                | Your Choice           | Multiplier |
                |------------------------|------------|
                | Default (neutral)      | 1.0        |
                | Somewhat important     | 1.25       |
                | Important              | 1.5        |
                | Very important         | 2.0        |
                | Exclude from scoring   | 0.0        |

                These weights are **normalized to sum to 1**, so the perfect possible health or environment score is also **1**.  
                To make scores easier to read, we convert them into **percentages from 0 to 100** in the app.

                ---
                ### 🧮 Default Weights Table

                Below is the list of default weights used to calculate the scores before any customization. These weights reflect the relative importance of each category in the total score:

                #### ⚖️ Overall Score Balance

                | Component            | Default Weight (%) |
                |----------------------|--------------------|
                | Health               | 50                 |
                | Environment          | 50                 |

                ---

                #### 🩺 Health Metrics (Total Weight = 1.00)

                | Metric Category              | Nutrient(s)                       | Default Weight |
                |------------------------------|-----------------------------------|----------------|
                | Macronutrients               | Protein, Carbohydrates, Fat       | 0.15 each      |
                |                              | Sugar                             | 0.10           |
                |                              | Saturated Fat, Trans Fat, Fibre   | 0.05 each      |
                | Micronutrients (Vitamins & Minerals) | All vitamins and minerals         | 0.0167 each     |

                > *Note: 0.0167 is the decimal approximation of 1/60.*

                ---

                #### 🌱 Environmental Metrics (Total Weight = 1.00)

                | Metric Type                  | Default Weight per Metric |
                |------------------------------|----------------------------|
                | All 11 Environmental Metrics | 0.0909 each               |

                > *Note: 0.0909 is the decimal approximation of 1/11.*
                ---

                ### 📌 Notes

                - You’ll always see **all metrics** listed for transparency.
                - However, if you choose to **exclude a metric**, it will not influence your scores.
                - This setup lets you customize scoring based on your own values and health goals.

                """)
with st.expander("💾 **Datasets**"):
    st.markdown("""
                - For the <b>environmental metrics</b>, we used the [Agribalyse Dataset](https://doc.agribalyse.fr/documentation-en)<br>
                - For the <b>micro-nutrient metrics</b> (including vitamins and minerals), we used the [NEVO Dataset](https://nevo-online.rivm.nl/)<br>
                - For the <b>recipes</b>, we used the [BBCGoodFood website](https://www.bbcgoodfood.com/)
                """, unsafe_allow_html=True)

with st.expander("📊 **How to read the bar charts?**"):
    st.markdown("""
    ### Nutritional Charts
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
    st.markdown("""
        ### Environmental Charts
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


    st.markdown("""
    ---
    ### 🎨 Color Scheme Explanation

    To help you interpret scores and values at a glance, we use a simple color coding system for nutritional and environmental metrics.

    ---

    #### 🥗 Nutritional Metrics

    Each nutrient in a recipe is compared to its **recommended daily intake** (or upper limit). Based on this comparison:

    | Color   | Meaning                         |
    |---------|---------------------------------|
    | 🟧 Orange | **Below** the recommended intake (potential deficiency) |
    | 🟩 Green  | **Within** the healthy recommended range                 |
    | 🟥 Red    | **Above** the recommended limit (potential excess)       |

    This helps identify where a meal may fall short or oversupply specific nutrients.

    ---

    #### 🌍 Environmental Metrics

    Each environmental metric (like CO₂, land use, or water use) is compared to a **threshold** or **median value**. The color reflects **how far the value deviates** from what’s considered reasonable:

    | Situation       | Color                        | Description                                |
    |-----------------|------------------------------|--------------------------------------------|
    | Well below      | 🟩 Green                     | Low-impact; much better than threshold     |
    | Slightly below  | 🟧 Orange                    | Still good, but close to average/limit     |
    | Above threshold | 🟥 Red                       | Higher-than-desired environmental impact   |

    We use a **gradient** between green and red to reflect the degree of deviation — so even within the same color range, **lighter or darker tones** may signal how close or far the value is from the benchmark.

    """)
