import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="AI Plant Nutrient Monitoring",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI-Based Plant Nutrient Monitoring")
st.write("Real-Time Plant Problem and Nutrient Deficiency Analysis")

st.divider()

# =====================================================
# IMAGE INPUT
# =====================================================

st.header("📷 Plant Image Analysis")

image = st.camera_input("Take a picture of the plant")

uploaded_image = st.file_uploader(
    "Or upload a plant image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:
    image = uploaded_image

if image is not None:

    st.image(
        image,
        caption="Plant Image",
        use_container_width=True
    )

    st.success("✅ Plant image received")

    st.info(
        "AI visual analysis will identify visible plant symptoms "
        "and estimate possible nutrient deficiencies."
    )

else:

    st.warning(
        "Please capture or upload a plant image."
    )

st.divider()

# =====================================================
# SOIL PARAMETERS
# =====================================================

st.header("🌍 Soil Parameters")

col1, col2, col3 = st.columns(3)

ph = col1.number_input(
    "Soil pH",
    min_value=0.0,
    max_value=14.0,
    value=6.5
)

moisture = col2.number_input(
    "Moisture (%)",
    min_value=0.0,
    max_value=100.0,
    value=48.0
)

temperature = col3.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=60.0,
    value=27.0
)

st.divider()

# =====================================================
# MICRONUTRIENT INPUT
# =====================================================

st.header("🧪 Soil Micronutrient Data")

col1, col2, col3 = st.columns(3)

fe = col1.number_input(
    "Iron Fe",
    value=18.0
)

zn = col2.number_input(
    "Zinc Zn",
    value=15.0
)

boron = col3.number_input(
    "Boron B",
    value=0.4
)

col1, col2, col3 = st.columns(3)

mn = col1.number_input(
    "Manganese Mn",
    value=20.0
)

cu = col2.number_input(
    "Copper Cu",
    value=2.1
)

mo = col3.number_input(
    "Molybdenum Mo",
    value=0.18
)

# =====================================================
# DEFICIENCY ANALYSIS
# =====================================================

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

    if value < minimum:
        status = "LOW"
    else:
        status = "NORMAL"

    results.append({
        "Nutrient": nutrient,
        "Value": value,
        "Status": status
    })

nutrient_df = pd.DataFrame(results)

# =====================================================
# NUTRIENT STATUS
# =====================================================

st.header("🧪 Micronutrient Status")

st.dataframe(
    nutrient_df,
    use_container_width=True,
    hide_index=True
)

deficiencies = nutrient_df[
    nutrient_df["Status"] == "LOW"
]["Nutrient"].tolist()

st.divider()

# =====================================================
# DEFICIENCY ALERT
# =====================================================

st.header("🚨 Deficiency Detection")

if deficiencies:

    st.error(
        "Possible nutrient deficiency: "
        + ", ".join(deficiencies)
    )

else:

    st.success(
        "All monitored nutrients are within the prototype range."
    )

# =====================================================
# IMAGE ANALYSIS SIMULATION
# =====================================================

st.header("🤖 AI Image Analysis")

if image is not None:

    st.info(
        "Image analysis module is active. "
        "Connect an AI vision model to obtain image-based diagnosis."
    )

    st.subheader("🌱 Visual Diagnosis")

    st.write(
        "Possible plant stress detected from image."
    )

    st.write(
        "The visual result should be treated as an AI estimate "
        "and confirmed using soil/sensor measurements."
    )

    st.subheader("🔍 Possible Problems")

    if deficiencies:

        for deficiency in deficiencies:

            if deficiency == "Iron (Fe)":
                st.warning(
                    "Possible Iron deficiency: leaf yellowing/chlorosis may be associated with low iron."
                )

            elif deficiency == "Zinc (Zn)":
                st.warning(
                    "Possible Zinc deficiency: abnormal growth or leaf symptoms may be associated with low zinc."
                )

            elif deficiency == "Boron (B)":
                st.warning(
                    "Possible Boron deficiency: abnormal young tissue/growth symptoms may be associated with low boron."
                )

            elif deficiency == "Manganese (Mn)":
                st.warning(
                    "Possible Manganese deficiency: interveinal chlorosis may be associated with low manganese."
                )

            elif deficiency == "Copper (Cu)":
                st.warning(
                    "Possible Copper deficiency: young leaf and shoot symptoms may be associated with low copper."
                )

            elif deficiency == "Molybdenum (Mo)":
                st.warning(
                    "Possible Molybdenum deficiency: leaf symptoms may be associated with low molybdenum."
                )

    else:

        st.success(
            "No nutrient deficiency detected from the current soil data."
        )

else:

    st.info(
        "Upload/capture a plant image to start visual analysis."
    )

st.divider()

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

    for deficiency in deficiencies:

        st.warning(
            "➡️ " + recommendations[deficiency]
        )

else:

    st.success(
        "No supplement recommendation required for the current prototype reading."
    )

st.divider()

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

    if nutrient in deficiencies:
        status = "ON"
    else:
        status = "OFF"

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

st.divider()

# =====================================================
# GRAPH
# =====================================================

st.header("📊 Nutrient Monitoring Graph")

graph_df = nutrient_df.set_index("Nutrient")[["Value"]]

st.bar_chart(graph_df)

st.divider()

# =====================================================
# SYSTEM STATUS
# =====================================================

st.header("📡 System Status")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Image",
    "Received" if image is not None else "Waiting"
)

c2.metric(
    "Deficiencies",
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

# =====================================================
# SYSTEM FLOW
# =====================================================

st.header("🔄 System Flow")

st.write(
    "📷 Plant Image → 🤖 AI Image Analysis → "
    "🌱 Problem Identification → 🧪 Nutrient Analysis → "
    "🚨 Deficiency Detection → 💡 Recommendation → "
    "⚙️ Pump Simulation"
)
