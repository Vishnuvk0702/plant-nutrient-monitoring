import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Plant Micronutrient Monitoring",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Real-Time Plant Micronutrient Monitoring")
st.write("Intelligent Supplement System for Precision Agriculture")

st.divider()

# -----------------------------
# SENSOR INPUT
# -----------------------------

st.header("📡 Sensor Data")

col1, col2, col3 = st.columns(3)

with col1:
    ph = st.number_input("Soil pH", 0.0, 14.0, 6.5, 0.1)

with col2:
    moisture = st.number_input("Soil Moisture (%)", 0, 100, 48)

with col3:
    temperature = st.number_input("Temperature (°C)", 0, 60, 27)

st.divider()

# -----------------------------
# MICRONUTRIENT INPUT
# -----------------------------

st.header("🧪 Micronutrient Sensor Values")

col1, col2, col3 = st.columns(3)

with col1:
    fe = st.number_input("Iron (Fe)", 0.0, 200.0, 18.0)
    zn = st.number_input("Zinc (Zn)", 0.0, 200.0, 15.0)

with col2:
    boron = st.number_input("Boron (B)", 0.0, 20.0, 0.4)
    mn = st.number_input("Manganese (Mn)", 0.0, 300.0, 20.0)

with col3:
    cu = st.number_input("Copper (Cu)", 0.0, 50.0, 2.1)
    mo = st.number_input("Molybdenum (Mo)", 0.0, 20.0, 0.18)

# -----------------------------
# PROTOTYPE THRESHOLDS
# -----------------------------

minimum_values = {
    "Iron (Fe)": 20,
    "Zinc (Zn)": 15,
    "Boron (B)": 0.5,
    "Manganese (Mn)": 20,
    "Copper (Cu)": 2,
    "Molybdenum (Mo)": 0.2
}

values = {
    "Iron (Fe)": fe,
    "Zinc (Zn)": zn,
    "Boron (B)": boron,
    "Manganese (Mn)": mn,
    "Copper (Cu)": cu,
    "Molybdenum (Mo)": mo
}

# -----------------------------
# STATUS DETECTION
# -----------------------------

status = {}

for nutrient in values:

    if values[nutrient] < minimum_values[nutrient]:
        status[nutrient] = "LOW"
    else:
        status[nutrient] = "NORMAL"

st.divider()

# -----------------------------
# MICRONUTRIENT STATUS
# -----------------------------

st.header("📊 Micronutrient Status")

data = []

for nutrient in values:

    data.append({
        "Nutrient": nutrient,
        "Value": values[nutrient],
        "Minimum": minimum_values[nutrient],
        "Status": status[nutrient]
    })

df = pd.DataFrame(data)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# DEFICIENCY DETECTION
# -----------------------------

deficiencies = [
    nutrient
    for nutrient in status
    if status[nutrient] == "LOW"
]

st.divider()

st.header("🚨 Deficiency Detection")

if deficiencies:

    st.error(
        "Deficiency detected: "
        + ", ".join(deficiencies)
    )

else:

    st.success(
        "All monitored micronutrients are within the prototype range."
    )

# -----------------------------
# RECOMMENDATION
# -----------------------------

recommendations = {
    "Iron (Fe)": "Iron Supplement",
    "Zinc (Zn)": "Zinc Supplement",
    "Boron (B)": "Boron Supplement",
    "Manganese (Mn)": "Manganese Supplement",
    "Copper (Cu)": "Copper Supplement",
    "Molybdenum (Mo)": "Molybdenum Supplement"
}

st.header("💡 Supplement Recommendation")

if deficiencies:

    for nutrient in deficiencies:

        st.warning(
            "➡️ " + recommendations[nutrient]
        )

else:

    st.success("No supplement required.")

# -----------------------------
# PUMP SIMULATION
# -----------------------------

st.divider()

st.header("⚙️ Actuator / Pump Simulation")

pump_mapping = {
    "Iron (Fe)": "Pump 1",
    "Zinc (Zn)": "Pump 2",
    "Boron (B)": "Pump 3",
    "Manganese (Mn)": "Pump 4",
    "Copper (Cu)": "Pump 5",
    "Molybdenum (Mo)": "Pump 6"
}

pump_data = []

for nutrient in pump_mapping:

    pump = pump_mapping[nutrient]

    if nutrient in deficiencies:
        pump_status = "ON"
    else:
        pump_status = "OFF"

    pump_data.append({
        "Pump": pump,
        "Supplement": nutrient,
        "Status": pump_status
    })

pump_df = pd.DataFrame(pump_data)

st.dataframe(
    pump_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# NUTRIENT GRAPH
# -----------------------------

st.divider()

st.header("📈 Nutrient Monitoring Graph")

chart_df = pd.DataFrame({
    "Nutrient": list(values.keys()),
    "Value": list(values.values())
})

chart_df = chart_df.set_index("Nutrient")

st.bar_chart(chart_df)

# -----------------------------
# SYSTEM SUMMARY
# -----------------------------

st.divider()

st.header("🌱 System Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Nutrients",
        len(values)
    )

with c2:
    st.metric(
        "Deficiencies",
        len(deficiencies)
    )

with c3:
    if deficiencies:
        st.metric("System Status", "ATTENTION")
    else:
        st.metric("System Status", "NORMAL")

st.info(
    "This is a software prototype using simulated sensor values. "
    "Actual sensors and agricultural reference values can be integrated later."
)
