import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
from PIL import Image
import plotly.express as px
from utils.simulation import generate_sensor_data
from utils.gauges import create_gauge
from utils.graphs import create_live_graph
from utils.animation import show_grid_status
from utils.scada_animation import show_scada_grid
from utils.report import generate_pdf
from utils.history_dashboard import show_history_dashboard
from utils.gis_map import show_gis_map
from utils.weather_api import get_weather_by_coordinates
from utils.advanced_gis import show_advanced_gis
from utils.control_room import control_room_header
from utils.plotly_gis import show_plotly_map
from utils.demo_mode import generate_demo_data
from streamlit_autorefresh import st_autorefresh
from utils.executive_dashboard import show_executive_dashboard
from utils.notification_center import show_notifications
from utils.animated_logo import show_animated_logo
from utils.startup_animation import startup_animation
from utils.cinematic_startup import cinematic_startup
from utils.scada_animation import show_scada_grid
from utils.alarm import play_alarm
st.set_page_config(
    page_title="GridGuard AI",
    page_icon="⚡",
    layout="wide"
)
if "boot_screen" not in st.session_state:
    cinematic_startup()
    st.session_state.boot_screen = True
st.caption(
    "🕒 " +
    datetime.now().strftime("%d %B %Y | %I:%M:%S %p")
)
#if "startup_complete" not in st.session_state:
    #cinematic_startup()
    #st.session_state.startup_complete = True
if "startup_done" not in st.session_state:
    st.session_state.startup_done = True
    startup_animation()  

if "fault" not in st.session_state:
    st.session_state["fault"] = "Normal"
# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# --------------------------------------------------
# Load AI Model
# --------------------------------------------------
model = joblib.load("fault_model.pkl")
encoder = joblib.load("fault_encoder.pkl")

# --------------------------------------------------
# Load Images
# --------------------------------------------------
try:
    transformer = Image.open("assets/transformer.png")
    pole = Image.open("assets/pole.png")
    house = Image.open("assets/house.png")
except:
    transformer = None
    pole = None
    house = None

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
if os.path.exists("assets/logo.png"):
    st.sidebar.image("assets/logo.png", width=120)


menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🗺️ Tamil Nadu GIS",
        "📋 Fault History",
        "📈 Analytics",
        "📄 Reports",
        "📊 Live Monitoring",
        "ℹ️ About"
    ]
)
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

# ==================================================
# DASHBOARD
# ==================================================
if menu == "🏠 Dashboard":

    show_animated_logo()

    demo = st.toggle("🎬 Presentation Demo Mode")

    st.markdown("---")

    mode = st.radio(
        "Choose Input Mode",
        ["Manual Input", "Live Simulation"],
        horizontal=True
    )

    
    fault = st.session_state.get("fault", "Normal")
    confidence = st.session_state.get("confidence", 0)

    show_executive_dashboard(
        fault,
        confidence
    )

    # ==========================================
    # INPUT MODES
    # ==========================================

    if demo:

        st_autorefresh(interval=1000, key="demo_refresh")

        sensor = generate_demo_data()

        voltage = sensor["Voltage"]
        current = sensor["Current"]
        frequency = sensor["Frequency"]
        temperature = sensor["Temperature"]

        fault = sensor["Fault"]
        confidence = sensor["Confidence"]

        st.session_state["fault"] = fault
        st.session_state["confidence"] = confidence

        st.success("🎬 Presentation Demo Mode Running")

    elif mode == "Manual Input":

        col1, col2 = st.columns(2)

        with col1:
            voltage = st.number_input("🔌 Voltage (V)", 0.0, value=230.0)
            current = st.number_input("⚡ Current (A)", 0.0, value=5.0)

        with col2:
            frequency = st.number_input("📡 Frequency (Hz)", 0.0, value=50.0)
            temperature = st.number_input("🌡 Temperature (°C)", 0.0, value=30.0)

    else:

        sensor = generate_sensor_data()

        voltage = sensor["Voltage"]
        current = sensor["Current"]
        frequency = sensor["Frequency"]
        temperature = sensor["Temperature"]

        st.info("⚡ Live Simulation Mode")
        st.session_state["voltage"] = voltage
        st.session_state["current"] = current
        st.session_state["frequency"] = frequency
        st.session_state["temperature"] = temperature

    # ==========================================
    # LIVE METRICS
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Voltage", f"{voltage} V")
    c2.metric("Current", f"{current} A")
    c3.metric("Frequency", f"{frequency} Hz")
    c4.metric("Temperature", f"{temperature} °C")

    # ==========================================
    # GAUGES
    # ==========================================

    st.subheader("📟 Live SCADA Gauges")

    g1, g2 = st.columns(2)

    with g1:
        st.plotly_chart(
            create_gauge("Voltage (V)", voltage, 0, 300),
            use_container_width=True
        )

    with g2:
        st.plotly_chart(
            create_gauge("Current (A)", current, 0, 20),
            use_container_width=True
        )

    g3, g4 = st.columns(2)

    with g3:
        st.plotly_chart(
            create_gauge("Frequency (Hz)", frequency, 45, 55),
            use_container_width=True
        )

    with g4:
        st.plotly_chart(
            create_gauge("Temperature (°C)", temperature, 0, 100),
            use_container_width=True
        )

    # ==========================================
    # NOTIFICATIONS
    # ==========================================

    st.markdown("---")
    show_notifications(fault)

    # ==========================================
    # LIVE SENSOR TRENDS
    # ==========================================

    st.markdown("---")
    st.subheader("📈 Live Sensor Trends")

# Store previous values
    if "voltage_history" not in st.session_state:
            st.session_state.voltage_history = []

    if "current_history" not in st.session_state:
            st.session_state.current_history = []

    if "frequency_history" not in st.session_state:
            st.session_state.frequency_history = []

    if "temperature_history" not in st.session_state:
            st.session_state.temperature_history = []

# Keep only last 20 readings
    st.session_state.voltage_history.append(voltage)
    st.session_state.current_history.append(current)
    st.session_state.frequency_history.append(frequency)
    st.session_state.temperature_history.append(temperature)

    st.session_state.voltage_history = st.session_state.voltage_history[-20:]
    st.session_state.current_history = st.session_state.current_history[-20:]
    st.session_state.frequency_history = st.session_state.frequency_history[-20:]
    st.session_state.temperature_history = st.session_state.temperature_history[-20:]

    g1, g2 = st.columns(2)

    with g1:
        st.plotly_chart(
        create_live_graph(
                    st.session_state.voltage_history,
                    "Voltage Trend",
                    "Voltage (V)"
                ),
                use_container_width=True
            )

    with g2:
            st.plotly_chart(
                create_live_graph(
                    st.session_state.current_history,
                    "Current Trend",
                    "Current (A)"
                ),
                use_container_width=True
            )

    g3, g4 = st.columns(2)

    with g3:
            st.plotly_chart(
                create_live_graph(
                    st.session_state.frequency_history,
                    "Frequency Trend",
                    "Frequency (Hz)"
                ),
                use_container_width=True
            )

    with g4:
            st.plotly_chart(
                create_live_graph(
                    st.session_state.temperature_history,
                    "Temperature Trend",
                    "Temperature (°C)"
                ),
                use_container_width=True
            )
    st.markdown("---")

    st.markdown("---")

    if st.button("🔍 Predict Fault", use_container_width=True):

   

        # ----------------------------
        # Prepare Input
        # ----------------------------
        
        new_data = pd.DataFrame({
            "Voltage": [voltage],
            "Current": [current],
            "Frequency": [frequency],
            "Temperature": [temperature]
        })

        prediction = model.predict(new_data)

        fault = encoder.inverse_transform(prediction)[0]

        confidence = model.predict_proba(new_data).max() * 100


     # Store fault
        st.session_state["fault"] = fault


     # ----------------------------
     # Display Result
     # ----------------------------

        st.success(f"⚡ Detected Fault: {fault}")

        st.info(f"🎯 Confidence: {confidence:.2f}%")


     # ----------------------------
     # Alarm Sound
     # ----------------------------

        sound_file = None


        if fault == "Overload":
            sound_file = "assets/overload.mp3"

        elif fault == "Overvoltage":
            sound_file = "assets/overvoltage.mp3"

        elif fault == "Undervoltage":
            sound_file = "assets/undervoltage.mp3"

        elif fault == "Line Break":
            sound_file = "assets/emergency.mp3"


        if sound_file:

            try:
                with open(sound_file, "rb") as audio_file:

                    st.audio(
                    audio_file.read(),
                    format="audio/mp3",
                    autoplay=True
                )

            except FileNotFoundError:
                st.warning(f"⚠ {sound_file} not found.")

        # ----------------------------
        # Grid Health Logic
        # ----------------------------
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

        # ----------------------------
        # Save History
        # ----------------------------
        history = pd.read_csv(history_file)

        new_record = pd.DataFrame({
                "Time":[datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
                "Voltage":[voltage],
                "Current":[current],
                "Frequency":[frequency],
                "Temperature":[temperature],
                "Fault":[fault],
                "Confidence":[round(confidence,2)],
                "Grid Health":[health],
                "Shutdown":[shutdown]
            })

        history = pd.concat([history,new_record],ignore_index=True)
        history.to_csv(history_file,index=False)

        st.success("Prediction Completed Successfully")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("⚠ Fault", fault)
        c2.metric("📊 Confidence", f"{confidence:.2f}%")
        c3.metric("💚 Grid Health", f"{health}%")
        c4.metric("🚨 Shutdown", shutdown)

        if shutdown=="YES":
                st.error("🚨 Emergency Shutdown Activated")
        else:
                st.success("🟢 Grid Operating Normally")

        st.markdown("---")
        st.subheader("⚡ SCADA Smart Grid")
        show_scada_grid(fault)
        
        st.markdown("---")
        st.subheader("💡 AI Recommendation")

        if fault == "Normal":
                st.success("""
            Grid operating normally.

            No maintenance required.
            """)

        elif fault == "Overload":
                st.error("""
            Reduce connected load immediately.

            Inspect transformer.
            """)

        elif fault == "Overvoltage":
                st.warning("""
            Check voltage regulator.

            Inspect supply line.
            """)

        elif fault == "Undervoltage":
                st.warning("""
            Inspect LT feeder.

            Check transformer output.
            """)

        else:
                st.error("""
            Inspect distribution pole.

            Repair broken line.

            Restore supply safely.
            """)    
            # =====================================
        # PDF Report
        # =====================================

        pdf = generate_pdf(
         voltage=voltage,
         current=current,
         frequency=frequency,
         temperature=temperature,
         fault=fault,
         confidence=confidence,
         health=health,
         shutdown=shutdown
         )

        with open(pdf, "rb") as file:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=file,
                    file_name=pdf,
                    mime="application/pdf",
                    use_container_width=True
                )

                # ==================================================
        # Smart Grid Visualization
        # ==================================================
        st.markdown("---")

        show_grid_status(fault)
        # ==================================================
# FAULT HISTORY PAGE
# ==================================================
elif menu == "📋 Fault History":

    st.title("📋 Fault History")

    history = pd.read_csv(history_file)

    if history.empty:
        st.info("No fault history available.")
    else:
        st.dataframe(history, use_container_width=True)

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download History",
            csv,
            "GridGuard_History.csv",
            "text/csv"
        )


# ==================================================
# ANALYTICS PAGE
# ==================================================
elif menu == "📈 Analytics":

    st.title("📈 Grid Analytics")
    show_history_dashboard(history_file)

    history = pd.read_csv(history_file)

    if history.empty:
        st.warning("No data available.")
    else:

        st.subheader("Voltage Trend")

        fig1 = px.line(
            history,
            x="Time",
            y="Voltage",
            markers=True,
            title="Voltage vs Time"
        )

        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Current Trend")

        fig2 = px.line(
            history,
            x="Time",
            y="Current",
            markers=True,
            title="Current vs Time"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Temperature Trend")

        fig3 = px.line(
            history,
            x="Time",
            y="Temperature",
            markers=True,
            title="Temperature vs Time"
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Fault Distribution")

        fig4 = px.pie(
            history,
            names="Fault",
            title="Detected Faults"
        )

        st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# Project Statistics
# --------------------------------------------------
        st.markdown("---")

        st.subheader("📊 Project Statistics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Predictions",
            len(history)
        )

        c2.metric(
            "Fault Types",
            history["Fault"].nunique()
        )

        c3.metric(
            "Average Grid Health",
            f"{history['Grid Health'].mean():.1f}%"
        )

# ==================================================
# REPORTS PAGE
# ==================================================
elif menu == "📄 Reports":

    st.title("📄 Reports")

    history = pd.read_csv(history_file)

    if history.empty:
        st.warning("No report available.")
    else:

        st.subheader("Latest Fault Report")

        latest = history.iloc[-1]

        st.write("### Prediction Summary")

        st.write(f"**Time:** {latest['Time']}")
        st.write(f"**Voltage:** {latest['Voltage']} V")
        st.write(f"**Current:** {latest['Current']} A")
        st.write(f"**Frequency:** {latest['Frequency']} Hz")
        st.write(f"**Temperature:** {latest['Temperature']} °C")
        st.write(f"**Fault:** {latest['Fault']}")
        st.write(f"**Confidence:** {latest['Confidence']} %")
        st.write(f"**Grid Health:** {latest['Grid Health']} %")
        st.write(f"**Shutdown:** {latest['Shutdown']}")

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Complete Report",
            csv,
            "GridGuard_Report.csv",
            "text/csv"
        )
        # ==================================================
# LIVE MONITORING
# ==================================================
elif menu == "📊 Live Monitoring":

    st.title("📊 Live Grid Monitoring")

    history = pd.read_csv(history_file)

    if history.empty:
        st.warning("No sensor data available.")
    else:

        latest = history.iloc[-1]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🔌 Voltage",
            f"{latest['Voltage']} V"
        )

        c2.metric(
            "⚡ Current",
            f"{latest['Current']} A"
        )

        c3.metric(
            "🌡 Temperature",
            f"{latest['Temperature']} °C"
        )

        c4.metric(
            "💚 Grid Health",
            f"{latest['Grid Health']} %"
        )

        st.markdown("---")

        st.subheader("Latest Fault")

        if latest["Shutdown"] == "YES":
            st.error(f"""
Fault : {latest['Fault']}

Emergency Shutdown Activated
""")
        else:
            st.success("Grid Operating Normally")
        # ==================================================
# ABOUT
# ==================================================
elif menu == "ℹ️ About":
    st.title("ℹ️ About GridGuard AI")

    st.markdown("""
# ⚡ GridGuard AI

GridGuard AI is an Artificial Intelligence based Low Tension (LT)
power distribution fault detection system.

The application predicts:

- Overload
- Overvoltage
- Undervoltage
- Line Break
- Normal

using Machine Learning.

---

## Technologies Used

- Python
- Streamlit
- Scikit-Learn
- Pandas
- Plotly
- Joblib

---

## Features

✅ AI Fault Prediction

✅ Emergency Shutdown

✅ Smart Grid Visualization

✅ Fault History

✅ Analytics Dashboard

✅ Reports

✅ Live Monitoring

---

Developed as an AI & ML Mini Project.
""")
    
elif menu == "🗺️ Tamil Nadu GIS":

    show_plotly_map()