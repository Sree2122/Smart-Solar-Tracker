import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Streamlit page setup
st.set_page_config(page_title="Solar Tracker Dashboard", layout="wide")
st.title("☀️ Solar Tracker Dashboard")

# File path
file_path = "solar_tracker_data.csv"

# Check if file exists
if not os.path.exists(file_path):
    st.warning("⚠️ CSV file not found. Please ensure 'solar_tracker_data.csv' is in the same folder.")
    st.stop()

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

# Try reading CSV
try:
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# Check if empty
if df.empty:
    st.warning("No data found yet. Run your tracker and let it log values.")
    st.stop()

# Expected columns in your file
expected_cols = ['Time', 'TL', 'TR', 'BL', 'BR', 'ServoX', 'ServoY']
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    st.error(f"Missing columns in CSV: {', '.join(missing)}")
    st.stop()

# Rename for convenience (internal use)
df = df.rename(columns={
    'Time': 'time',
    'TL': 'tl',
    'TR': 'tr',
    'BL': 'bl',
    'BR': 'br',
    'ServoX': 'servoX',
    'ServoY': 'servoY'
})

# Convert Unix time to readable format
df['timestamp'] = pd.to_datetime(df['time'], unit='s', errors='coerce')

# Compute Proxy Energy
df["proxy_energy"] = ((df["tl"] + df["tr"] + df["bl"] + df["br"]) / 4) * 0.001
df["cumulative_energy"] = df["proxy_energy"].cumsum()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 LDR Sensor Readings")
    fig1 = px.line(
        df,
        x="timestamp",
        y=["tl", "tr", "bl", "br"],
        title="LDR Intensity vs Time",
        labels={"timestamp": "Time", "value": "LDR Value"}
    )
    st.plotly_chart(fig1, use_container_width=True, key="ldr_chart")

with col2:
    st.subheader("⚙️ Servo Angles")
    fig2 = px.line(
        df,
        x="timestamp",
        y=["servoX", "servoY"],
        title="Servo X & Y Angles vs Time",
        labels={"timestamp": "Time", "value": "Angle (°)"}
    )
    st.plotly_chart(fig2, use_container_width=True, key="servo_chart")

st.divider()

# Proxy Energy charts
st.subheader("⚡ Proxy Energy Analysis")
col3, col4 = st.columns(2)

with col3:
    fig3 = px.line(
        df,
        x="timestamp",
        y="proxy_energy",
        title="Instantaneous Proxy Energy",
        labels={"timestamp": "Time", "proxy_energy": "Energy (arbitrary units)"}
    )
    st.plotly_chart(fig3, use_container_width=True, key="proxy_energy_chart")

with col4:
    fig4 = px.line(
        df,
        x="timestamp",
        y="cumulative_energy",
        title="Cumulative Proxy Energy",
        labels={"timestamp": "Time", "cumulative_energy": "Total Energy"}
    )
    st.plotly_chart(fig4, use_container_width=True, key="cumulative_chart")

# Summary stats
st.divider()
latest = df.iloc[-1]
st.metric("🌤️ Latest Proxy Energy", f"{latest['proxy_energy']:.4f}")
st.metric("🔁 Total Cumulative Energy", f"{latest['cumulative_energy']:.2f}")

st.success("✅ Dashboard updated successfully!")
st.caption("Tip: Click 'Refresh Data' whenever new readings are logged to the CSV.")
