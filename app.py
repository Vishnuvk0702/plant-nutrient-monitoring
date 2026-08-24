import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Plant Nutrient Monitoring",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Real-Time Plant Micronutrient Monitoring")
st.write("Intelligent Supplement System for Precision Agriculture")

st.divider()

# ---------------- CAMERA / IMAGE MODULE ----------------

st.subheader("📷 Real-Time Plant Image Simulation")

camera_image = st.camera_input("Capture Plant Image")

if camera_image:
    st.image(
        camera_image,
        caption="Live Plant Image Captured",
        use_container_width=True
    )

    st.success("✅ Plant image received for analysis")

else:
    st.info("📷 Open camera and capture the plant image")

st.divider()

# ---------------- SOIL PARAMETERS ----------------

st.subheader("🌍 Soil Parameters")

c1, c2, c3 = st.columns(3)

c1.metric("Soil pH", "6.5")
c2.metric("Moisture", "48%")
c3.metric("Temperature", "27°C")

st.divider()

# ---------------- NUTRIENT DATA ----------------

data = {
    "Nutrient": [
        "Iron (Fe)",
        "Zinc (Zn)",
        "Boron (B)",
        "Manganese (Mn)",
        "Copper (Cu)",
        "Molybdenum (Mo)"
    ],
    "Value": [18, 15, 0.4, 20, 2.1, 0.18],
    "Minimum": [20, 15, 0.5, 20, 2, 0.2]
}

df = pd.DataFrame(data)

df["Status"] = df.apply(
    lambda row: "LOW"
    if row["Value"] < row["Minimum"]
    else "NORMAL",
    axis=1
)

# ---------------- NUTRIENT STATUS ----------------

st.subheader("🧪 Micronutrient Status")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- DEFICIENCY ----------------

deficiencies = df[
    df["Status"] == "LOW"
]["Nutrient"].tolist()

st.subheader("🚨 Deficiency Detection")

if deficiencies:

    st.error(
        "Deficiency detected: " +
        ", ".join(deficiencies)
    )

else:

    st.success("All nutrients are normal.")

# ---------------- RECOMMENDATION ----------------

st.subheader("💡 Supplement Recommendation")

recommendations = {
    "Iron (Fe)": "Iron Supplement",
    "Zinc (Zn)": "Zinc Supplement",
    "Boron (B)": "Boron Supplement",
    "Manganese (Mn)": "Manganese Supplement",
    "Copper (Cu)": "Copper Supplement",
    "Molybdenum (Mo)": "Molybdenum Supplement"
}

if deficiencies:

    for nutrient in deficiencies:
        st.warning(
            "➡️ " + recommendations[nutrient]
        )

else:

    st.success("No supplement required.")

st.divider()

# ---------------- PUMP SIMULATION ----------------

st.subheader("⚙️ Actuator / Pump Simulation")

pump_mapping = {
    "Iron (Fe)": "Pump 1",
    "Zinc (Zn)": "Pump 2",
    "Boron (B)": "Pump 3",
    "Manganese (Mn)": "Pump 4",
    "Copper (Cu)": "Pump 5",
    "Molybdenum (Mo)": "Pump 6"
}

pump_data = []

for nutrient, pump in pump_mapping.items():

    status = "ON" if nutrient in deficiencies else "OFF"

    pump_data.append({
        "Pump": pump,
        "Supplement": nutrient,
        "Status": status
    })

pump_df = pd.DataFrame(pump_data)

st.dataframe(
    pump_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- GRAPH ----------------

st.subheader("📊 Nutrient Monitoring Graph")

chart_df = df.set_index("Nutrient")[["Value"]]

st.bar_chart(chart_df)

st.divider()

# ---------------- SYSTEM FLOW ----------------

st.subheader("🔄 System Flow")

st.write(
    "📷 Plant Image → 🌱 Plant Analysis → "
    "🧪 Nutrient Monitoring → 🚨 Deficiency Detection → "
    "💡 Supplement Recommendation → ⚙️ Pump Simulation"
)
