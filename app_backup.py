import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="GridGuard AI",
    page_icon="⚡",
    layout="wide"
)

# --------------------------------------------------
# Load AI Model
# --------------------------------------------------
model = joblib.load("fault_model.pkl")
encoder = joblib.load("fault_encoder.pkl")

# --------------------------------------------------
# Create History File
# --------------------------------------------------
history_file = "history.csv"

if not os.path.exists(history_file):
    history = pd.DataFrame(columns=[
        "Time",
        "Voltage",
        "Current",
        "Frequency",
        "Temperature",
        "Fault",
        "Confidence",
        "Grid Health",
        "Shutdown"
    ])
    history.to_csv(history_file, index=False)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("⚡ GridGuard AI")
st.subheader("AI-Based LT Line Fault Detection & Automatic Emergency Shutdown")

st.markdown("---")

# --------------------------------------------------
# Input Section
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    voltage = st.number_input(
        "🔌 Voltage (V)",
        min_value=0.0,
        value=230.0
    )

    current = st.number_input(
        "⚡ Current (A)",
        min_value=0.0,
        value=5.0
    )

with col2:
    frequency = st.number_input(
        "📡 Frequency (Hz)",
        min_value=0.0,
        value=50.0
    )

    temperature = st.number_input(
        "🌡 Temperature (°C)",
        min_value=0.0,
        value=30.0
    )

st.markdown("---")

# --------------------------------------------------
# Prediction
# --------------------------------------------------
if st.button("🔍 Predict Fault", use_container_width=True):

    new_data = pd.DataFrame({
        "Voltage": [voltage],
        "Current": [current],
        "Frequency": [frequency],
        "Temperature": [temperature]
    })

    prediction = model.predict(new_data)

    fault = encoder.inverse_transform(prediction)[0]

    confidence = model.predict_proba(new_data).max() * 100

    # Grid Health Logic
    if fault == "Normal":
        shutdown = "NO"
        health = 100

    elif fault == "Overload":
        shutdown = "YES"
        health = 45

    elif fault == "Overvoltage":
        shutdown = "YES"
        health = 40

    elif fault == "Undervoltage":
        shutdown = "YES"
        health = 50

    else:
        shutdown = "YES"
        health = 20

    # --------------------------------------------------
    # Save History
    # --------------------------------------------------
    history = pd.read_csv(history_file)

    new_record = pd.DataFrame({
        "Time": [datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
        "Voltage": [voltage],
        "Current": [current],
        "Frequency": [frequency],
        "Temperature": [temperature],
        "Fault": [fault],
        "Confidence": [round(confidence, 2)],
        "Grid Health": [health],
        "Shutdown": [shutdown]
    })

    history = pd.concat([history, new_record], ignore_index=True)

    history.to_csv(history_file, index=False)

    st.success("Prediction Completed Successfully")

    st.markdown("---")

    # --------------------------------------------------
    # Dashboard Cards
    # --------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⚠ Fault Type", fault)

    c2.metric("📊 Confidence", f"{confidence:.2f}%")

    c3.metric("💚 Grid Health", f"{health}%")

    c4.metric("🚨 Shutdown", shutdown)

    st.markdown("---")

    if shutdown == "YES":
        st.error("🚨 EMERGENCY SHUTDOWN ACTIVATED")
    else:
        st.success("🟢 SYSTEM OPERATING NORMALLY")

# --------------------------------------------------
# History Section
# --------------------------------------------------
history = pd.read_csv(history_file)

st.markdown("---")
st.subheader("📋 Fault History")

st.dataframe(history, use_container_width=True)

# --------------------------------------------------
# Download History
# --------------------------------------------------
csv = history.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Fault History",
    csv,
    "GridGuard_History.csv",
    "text/csv"
)

# --------------------------------------------------
# Charts
# --------------------------------------------------
if not history.empty:

    st.markdown("---")
    st.subheader("📈 Sensor Trends")

    fig1 = px.line(
        history,
        x="Time",
        y="Voltage",
        title="Voltage Trend",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        history,
        x="Time",
        y="Current",
        title="Current Trend",
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(
        history,
        x="Time",
        y="Temperature",
        title="Temperature Trend",
        markers=True
    )

    st.plotly_chart(fig3, use_container_width=True)