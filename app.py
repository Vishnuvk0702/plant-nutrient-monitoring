import streamlit as st
import pandas as pd
from PIL import Image
from google import genai
from google.genai import types
import json
import re

st.set_page_config(
    page_title="AI Plant Nutrient Monitoring",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI Plant Nutrient Monitoring System")
st.write("Image-Based Plant Problem and Nutrient Deficiency Analysis")

st.divider()

# =====================================================
# AI CLIENT
# =====================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# =====================================================
# IMAGE INPUT
# =====================================================

st.header("📷 Plant Image Input")

camera_image = st.camera_input(
    "Take a picture of the plant"
)

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

    st.success("✅ Image received")

else:

    st.info(
        "Upload or capture a plant image to start AI analysis."
    )

# =====================================================
# AI IMAGE ANALYSIS
# =====================================================

if image_file:

    if st.button("🤖 Analyze Plant Image"):

        with st.spinner("AI is analyzing the plant image..."):

            prompt = """
You are an agricultural plant-health image analysis assistant.

Analyze ONLY the plant shown in the image.

Return ONLY valid JSON using this structure:

{
  "plant_condition": "",
  "visible_problem": "",
  "possible_deficiency": "",
  "confidence": 0,
  "reason": "",
  "recommendation": ""
}

Rules:

1. Identify visible symptoms from the image.
2. If the plant appears healthy, say:
   "No obvious visible problem"
   and "No clear nutrient deficiency visible".
3. Do not invent a deficiency.
4. Nutrient deficiency from an image is only a POSSIBLE diagnosis.
5. Do not claim a nutrient deficiency is confirmed.
6. Mention the likely deficiency only when the visible symptoms reasonably support it.
7. Confidence must be between 0 and 100.
8. Give a short reason based on visible symptoms.
9. Give a cautious recommendation to confirm using soil/plant testing.
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

                st.session_state["ai_result"] = result

            except Exception as e:

                st.error(
                    "AI analysis failed: " + str(e)
                )

# =====================================================
# DISPLAY AI RESULT
# =====================================================

if "ai_result" in st.session_state:

    result = st.session_state["ai_result"]

    st.divider()

    st.header("🤖 AI Image Analysis Result")

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("🌱 Plant Condition")

        st.write(
            result.get(
                "plant_condition",
                "Not available"
            )
        )

        st.subheader("🔍 Visible Problem")

        st.write(
            result.get(
                "visible_problem",
                "Not available"
            )
        )

    with c2:

        st.subheader("🧪 Possible Deficiency")

        st.warning(
            result.get(
                "possible_deficiency",
                "No clear deficiency"
            )
        )

        st.subheader("📊 AI Confidence")

        st.metric(
            "Confidence",
            str(result.get("confidence", 0)) + "%"
        )

    st.subheader("🔎 Reason")

    st.write(
        result.get(
            "reason",
            "No explanation available"
        )
    )

    st.subheader("💡 Recommendation")

    st.info(
        result.get(
            "recommendation",
            "Confirm using appropriate soil or plant testing."
        )
    )

st.divider()

# =====================================================
# SOIL DATA
# =====================================================

st.header("🌍 Soil Parameters")

c1, c2, c3 = st.columns(3)

ph = c1.number_input(
    "Soil pH",
    min_value=0.0,
    max_value=14.0,
    value=6.5
)

moisture = c2.number_input(
    "Moisture (%)",
    min_value=0.0,
    max_value=100.0,
    value=48.0
)

temperature = c3.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=60.0,
    value=27.0
)

st.divider()

# =====================================================
# NUTRIENT DATA
# =====================================================

st.header("🧪 Soil Micronutrient Data")

c1, c2, c3 = st.columns(3)

fe = c1.number_input("Iron Fe", value=18.0)
zn = c2.number_input("Zinc Zn", value=15.0)
boron = c3.number_input("Boron B", value=0.4)

c1, c2, c3 = st.columns(3)

mn = c1.number_input("Manganese Mn", value=20.0)
cu = c2.number_input("Copper Cu", value=2.1)
mo = c3.number_input("Molybdenum Mo", value=0.18)

nutrients = {
    "Iron (Fe)": [fe, 20],
    "Zinc (Zn)": [zn, 15],
    "Boron (B)": [boron, 0.5],
    "Manganese (Mn)": [mn, 20],
    "Copper (Cu)": [cu, 2],
    "Molybdenum (Mo)": [mo, 0.2]
}

results = []

for nutrient, values in nutrients.items():

    value = values[0]
    minimum = values[1]

    status = "LOW" if value < minimum else "NORMAL"

    results.append({
        "Nutrient": nutrient,
        "Value": value,
        "Status": status
    })

nutrient_df = pd.DataFrame(results)

st.subheader("📊 Current Nutrient Status")

st.dataframe(
    nutrient_df,
    use_container_width=True,
    hide_index=True
)

deficiencies = nutrient_df[
    nutrient_df["Status"] == "LOW"
]["Nutrient"].tolist()

# =====================================================
# DEFICIENCY
# =====================================================

st.header("🚨 Soil-Based Deficiency Detection")

if deficiencies:

    st.error(
        "Low nutrient detected: "
        + ", ".join(deficiencies)
    )

else:

    st.success(
        "No low nutrient detected from current soil data."
    )

# =====================================================
# COMBINED DECISION
# =====================================================

st.divider()

st.header("🧠 Combined System Decision")

if "ai_result" in st.session_state:

    ai_deficiency = st.session_state[
        "ai_result"
    ].get(
        "possible_deficiency",
        ""
    )

    st.write(
        "**AI Visual Assessment:**"
    )

    st.write(ai_deficiency)

    st.write(
        "**Soil Data Assessment:**"
    )

    if deficiencies:

        st.write(
            ", ".join(deficiencies)
        )

    else:

        st.write("No low nutrient detected.")

else:

    st.info(
        "Analyze a plant image to obtain the AI visual assessment."
    )

# =====================================================
# RECOMMENDATION
# =====================================================

st.header("💡 Supplement Recommendation")

recommendations = {
    "Iron (Fe)": "Iron supplement",
    "Zinc (Zn)": "Zinc supplement",
    "Boron (B)": "Boron supplement",
    "Manganese (Mn)": "Manganese supplement",
    "Copper (Cu)": "Copper supplement",
    "Molybdenum (Mo)": "Molybdenum supplement"
}

if deficiencies:

    for item in deficiencies:

        st.warning(
            "➡️ " + recommendations[item]
        )

else:

    st.success(
        "No supplement recommendation from current soil values."
    )

# =====================================================
# PUMP SIMULATION
# =====================================================

st.header("⚙️ Actuator / Pump Simulation")

pump_mapping = {
    "Iron (Fe)": "Pump 1",
    "Zinc (Zn)": "Pump 2",
    "Boron (B)": "Pump 3",
    "Manganese (Mn)": "Pump 4",
    "Copper (Cu)": "Pump 5",
    "Molybdenum (Mo)": "Pump 6"
}

pump_results = []

for nutrient, pump in pump_mapping.items():

    status = (
        "ON"
        if nutrient in deficiencies
        else "OFF"
    )

    pump_results.append({
        "Pump": pump,
        "Supplement": nutrient,
        "Status": status
    })

pump_df = pd.DataFrame(pump_results)

st.dataframe(
    pump_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# GRAPH
# =====================================================

st.header("📈 Nutrient Monitoring")

graph_df = nutrient_df.set_index(
    "Nutrient"
)[["Value"]]

st.bar_chart(graph_df)

# =====================================================
# SYSTEM STATUS
# =====================================================

st.divider()

st.header("📡 System Status")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Image",
    "Ready" if image_file else "Waiting"
)

c2.metric(
    "Soil Deficiencies",
    len(deficiencies)
)

c3.metric(
    "Active Pumps",
    len(deficiencies)
)

c4.metric(
    "Soil pH",
    ph
)

st.divider()

st.caption(
    "AI image results are visual estimates and should be confirmed "
    "with appropriate agricultural testing before applying supplements."
)
