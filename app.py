import streamlit as st
import pandas as pd
from PIL import Image
from google import genai
from google.genai import types
import json
import re

st.set_page_config(
    page_title="AI Plant Micronutrient Monitoring",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI Plant Micronutrient Monitoring System")
st.write("Image-Based Plant Micronutrient Estimation")

# =====================================================
# GEMINI
# =====================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# =====================================================
# IMAGE
# =====================================================

st.header("📷 Plant Image")

camera_image = st.camera_input("Take a picture of the plant")

uploaded_image = st.file_uploader(
    "Or upload a plant image",
    type=["jpg", "jpeg", "png"]
)

image_file = uploaded_image if uploaded_image else camera_image

if image_file:

    image = Image.open(image_file)

    st.image(
        image,
        caption="Input Plant Image",
        use_container_width=True
    )

    if st.button("🤖 Analyze Micronutrients"):

        with st.spinner("Analyzing plant..."):

            prompt = """
You are an agricultural plant image analysis AI.

Analyze ONLY the plant shown in the image.

Estimate the possible micronutrient status from visible
leaf colour, chlorosis, necrosis, leaf deformation and
other visible symptoms.

Return ONLY valid JSON.

Use this exact structure:

{
  "plant_name": "",
  "plant_condition": "",
  "visible_problem": "",
  "possible_deficiency": "",
  "confidence": 0,

  "micronutrients": {
    "Iron_Fe": {
      "estimated_value": 0,
      "status": "",
      "unit": "mg/kg"
    },
    "Zinc_Zn": {
      "estimated_value": 0,
      "status": "",
      "unit": "mg/kg"
    },
    "Boron_B": {
      "estimated_value": 0,
      "status": "",
      "unit": "mg/kg"
    },
    "Manganese_Mn": {
      "estimated_value": 0,
      "status": "",
      "unit": "mg/kg"
    },
    "Copper_Cu": {
      "estimated_value": 0,
      "status": "",
      "unit": "mg/kg"
    },
    "Molybdenum_Mo": {
      "estimated_value": 0,
      "status": "",
      "unit": "mg/kg"
    }
  },

  "reason": "",
  "recommendation": ""
}

IMPORTANT RULES:

1. Analyze the actual plant in the image.
2. Do NOT return the same micronutrient values for every plant.
3. Values must vary according to visible plant symptoms.
4. If a nutrient deficiency is not visually supported,
   mark its status as "NORMAL".
5. Do not claim that image analysis is a laboratory measurement.
6. The micronutrient values are ESTIMATED values only.
7. Use realistic-looking different values for different plants.
8. Confidence must be between 0 and 100.
9. If the plant looks healthy, do not invent a deficiency.
10. Give a short explanation based only on visible symptoms.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[
                        types.Part.from_bytes(
                            data=image_file.getvalue(),
                            mime_type=image_file.type
                        ),
                        prompt
                    ]
                )

                text = response.text.strip()

                text = re.sub(
                    r"```json|```",
                    "",
                    text
                ).strip()

                result = json.loads(text)

                st.session_state["plant_result"] = result

            except Exception as e:

                st.error(
                    "AI analysis failed: " + str(e)
                )

# =====================================================
# RESULT
# =====================================================

if "plant_result" in st.session_state:

    result = st.session_state["plant_result"]

    st.divider()

    st.header("🤖 AI Image Analysis Result")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Plant",
        result.get("plant_name", "Unknown")
    )

    c2.metric(
        "Condition",
        result.get("plant_condition", "Unknown")
    )

    c3.metric(
        "Confidence",
        str(result.get("confidence", 0)) + "%"
    )

    st.subheader("🔍 Visible Problem")

    st.write(
        result.get(
            "visible_problem",
            "No obvious problem"
        )
    )

    st.subheader("🧪 Possible Deficiency")

    st.warning(
        result.get(
            "possible_deficiency",
            "No clear deficiency"
        )
    )

    st.subheader("🔎 Reason")

    st.write(
        result.get(
            "reason",
            "Not available"
        )
    )

    # =================================================
    # MICRONUTRIENTS
    # =================================================

    st.divider()

    st.header("🧪 Estimated Micronutrient Monitoring")

    micro = result.get(
        "micronutrients",
        {}
    )

    rows = []

    for name, data in micro.items():

        rows.append({
            "Micronutrient": name,
            "Estimated Value": data.get(
                "estimated_value",
                0
            ),
            "Unit": data.get(
                "unit",
                "mg/kg"
            ),
            "Status": data.get(
                "status",
                "NORMAL"
            )
        })

    nutrient_df = pd.DataFrame(rows)

    st.dataframe(
        nutrient_df,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # LOW NUTRIENTS
    # =================================================

    st.header("🚨 Micronutrient Deficiency")

    low = nutrient_df[
        nutrient_df["Status"].str.upper() == "LOW"
    ]

    if len(low) > 0:

        for nutrient in low["Micronutrient"]:

            st.error(
                "Low micronutrient detected: "
                + nutrient
            )

    else:

        st.success(
            "No visually estimated micronutrient deficiency detected."
        )

    # =================================================
    # RECOMMENDATION
    # =================================================

    st.header("💡 Supplement Recommendation")

    supplement_map = {

        "Iron_Fe":
            "Iron supplement",

        "Zinc_Zn":
            "Zinc supplement",

        "Boron_B":
            "Boron supplement",

        "Manganese_Mn":
            "Manganese supplement",

        "Copper_Cu":
            "Copper supplement",

        "Molybdenum_Mo":
            "Molybdenum supplement"
    }

    if len(low) > 0:

        for nutrient in low["Micronutrient"]:

            if nutrient in supplement_map:

                st.warning(
                    "➡️ " +
                    supplement_map[nutrient]
                )

    else:

        st.success(
            "No supplement recommendation."
        )

    # =================================================
    # PUMP
    # =================================================

    st.header("⚙️ Actuator / Pump Simulation")

    pump_map = {

        "Iron_Fe": "Pump 1",

        "Zinc_Zn": "Pump 2",

        "Boron_B": "Pump 3",

        "Manganese_Mn": "Pump 4",

        "Copper_Cu": "Pump 5",

        "Molybdenum_Mo": "Pump 6"
    }

    pump_rows = []

    for nutrient, pump in pump_map.items():

        status = "OFF"

        if nutrient in low["Micronutrient"].values:

            status = "ON"

        pump_rows.append({

            "Pump": pump,

            "Micronutrient": nutrient,

            "Status": status
        })

    pump_df = pd.DataFrame(
        pump_rows
    )

    st.dataframe(
        pump_df,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # GRAPH
    # =================================================

    st.header("📊 Micronutrient Monitoring Graph")

    chart_df = nutrient_df[
        ["Micronutrient", "Estimated Value"]
    ].set_index(
        "Micronutrient"
    )

    st.bar_chart(chart_df)

    # =================================================
    # SYSTEM STATUS
    # =================================================

    st.divider()

    st.header("📡 System Status")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Image",
        "Analyzed"
    )

    c2.metric(
        "Micronutrients",
        len(nutrient_df)
    )

    c3.metric(
        "Low Nutrients",
        len(low)
    )

    c4.metric(
        "Active Pumps",
        len(low)
    )

    st.divider()

    st.caption(
        "Micronutrient values shown here are AI-based visual "
        "estimates from the plant image and are not laboratory "
        "measurements. Confirm nutrient levels using appropriate "
        "soil or plant testing before applying supplements."
    )
