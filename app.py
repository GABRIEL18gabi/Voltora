import os
from datetime import datetime

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from streamlit_autorefresh import st_autorefresh

# ============================================================
# GRIDGUARD MODULES
# ============================================================

from utils.simulation import generate_sensor_data
from utils.virtual_circuit import simulate_circuit, get_circuit_status
from utils.virtual_sensors import read_virtual_sensors
from utils.circuit_builder import show_circuit_builder

from utils.gauges import create_gauge
from utils.graphs import create_live_graph
from utils.animation import show_grid_status
from utils.scada_animation import show_scada_grid

from utils.report import generate_pdf
from utils.history_dashboard import show_history_dashboard

from utils.weather_api import get_weather_by_coordinates
from utils.plotly_gis import show_plotly_map

from utils.executive_dashboard import show_executive_dashboard
from utils.notification_center import show_notifications

from utils.animated_logo import show_animated_logo
from utils.startup_animation import startup_animation
from utils.cinematic_startup import cinematic_startup

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GridGuard AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

def load_css():
    css_file = "assets/style.css"

    if os.path.exists(css_file):
        try:
            with open(css_file, "r", encoding="utf-8") as f:
                st.markdown(
                    f"<style>{f.read()}</style>",
                    unsafe_allow_html=True,
                )
        except Exception as exc:
            st.warning(f"Could not load CSS: {exc}")


load_css()


# ============================================================
# STARTUP
# ============================================================

if "boot_screen" not in st.session_state:
    st.session_state.boot_screen = True

    try:
        cinematic_startup()
    except Exception:
        pass


if "startup_done" not in st.session_state:
    st.session_state.startup_done = True

    try:
        startup_animation()
    except Exception:
        pass


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_SESSION = {
    "fault": "Normal",
    "confidence": 0.0,
    "health": 100,
    "shutdown": "NO",
    "voltage": 230.0,
    "current": 5.0,
    "frequency": 50.0,
    "temperature": 30.0,
    "last_asset_id": None,
    "last_line_id": None,
    "last_area_id": None,
}


for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# MODEL LOADING
# ============================================================

@st.cache_resource
def load_ai_model():

    model_path = "fault_model.pkl"
    encoder_path = "fault_encoder.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"{model_path} was not found in the project root."
        )

    if not os.path.exists(encoder_path):
        raise FileNotFoundError(
            f"{encoder_path} was not found in the project root."
        )

    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)

    return model, encoder


try:

    model, encoder = load_ai_model()

    model_error = None

except Exception as exc:

    model = None
    encoder = None
    model_error = str(exc)


# ============================================================
# OPTIONAL IMAGES
# ============================================================

try:
    transformer_image = Image.open(
        "assets/transformer.png"
    )
except Exception:
    transformer_image = None


try:
    pole_image = Image.open(
        "assets/pole.png"
    )
except Exception:
    pole_image = None


try:
    house_image = Image.open(
        "assets/house.png"
    )
except Exception:
    house_image = None


# ============================================================
# HISTORY FILE
# ============================================================

history_file = "history.csv"

HISTORY_COLUMNS = [
    "Time",
    "Area",
    "Line ID",
    "Asset ID",
    "Voltage",
    "Current",
    "Frequency",
    "Temperature",
    "Fault",
    "Confidence",
    "Grid Health",
    "Shutdown",
]


def initialize_history():

    if not os.path.exists(history_file):

        history = pd.DataFrame(
            columns=HISTORY_COLUMNS
        )

        history.to_csv(
            history_file,
            index=False,
        )


initialize_history()


# ============================================================
# SIDEBAR
# ============================================================

if os.path.exists("assets/logo.png"):

    try:
        st.sidebar.image(
            "assets/logo.png",
            width=120,
        )
    except Exception:
        pass


st.sidebar.markdown(
    "## ⚡ GridGuard AI"
)


menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🗺️ Tamil Nadu GIS",
        "📋 Fault History",
        "📈 Analytics",
        "📄 Reports",
        "📊 Live Monitoring",
        "ℹ️ About",
    ],
)


# ============================================================
# CURRENT TIME
# ============================================================

st.caption(
    "🕒 "
    + datetime.now().strftime(
        "%d %B %Y | %I:%M:%S %p"
    )
)


# ============================================================
# AI PREDICTION FUNCTION
# ============================================================

def predict_fault(
    voltage,
    current,
    frequency,
    temperature,
):
    """
    Run the EXISTING GridGuard AI model.

    Important:
    The AI receives only V/I/F/T values.

    It does NOT use circuit_condition as
    the prediction result.
    """

    if model is None or encoder is None:

        raise RuntimeError(
            model_error
            or "AI model is unavailable."
        )

    new_data = pd.DataFrame(
        {
            "Voltage": [float(voltage)],
            "Current": [float(current)],
            "Frequency": [float(frequency)],
            "Temperature": [float(temperature)],
        }
    )

    prediction = model.predict(
        new_data
    )

    fault = encoder.inverse_transform(
        prediction
    )[0]

    confidence = 0.0

    if hasattr(
        model,
        "predict_proba",
    ):

        probabilities = model.predict_proba(
            new_data
        )

        confidence = (
            float(probabilities.max())
            * 100
        )

    return str(fault), confidence


# ============================================================
# GRID HEALTH
# ============================================================

def calculate_grid_health(fault):

    fault = str(fault)

    if fault == "Normal":

        return 100, "NO"

    if fault == "Overload":

        return 45, "YES"

    if fault == "Overvoltage":

        return 40, "YES"

    if fault == "Undervoltage":

        return 50, "YES"

    if fault == "Line Break":

        return 20, "YES"

    return 30, "YES"


# ============================================================
# RECOMMENDATION
# ============================================================

def show_recommendation(fault):

    if fault == "Normal":

        st.success(
            """
            🟢 Grid operating normally.

            No immediate maintenance action required.
            """
        )

    elif fault == "Overload":

        st.error(
            """
            ⚠️ Reduce connected load immediately.

            Inspect transformer and feeder loading.
            """
        )

    elif fault == "Overvoltage":

        st.warning(
            """
            ⚠️ Check voltage regulator.

            Inspect incoming supply and transformer output.
            """
        )

    elif fault == "Undervoltage":

        st.warning(
            """
            ⚠️ Inspect LT feeder.

            Check transformer output and feeder voltage drop.
            """
        )

    elif fault == "Line Break":

        st.error(
            """
            🚨 Inspect distribution line.

            Locate the affected conductor section and
            restore supply only after the line is confirmed safe.
            """
        )

    else:

        st.warning(
            """
            ⚠️ Inspect the affected feeder and protection system.
            """
        )


# ============================================================
# ALARM
# ============================================================

def show_fault_alarm(fault):

    sound_file = None

    if fault == "Overload":

        sound_file = "assets/overload.mp3"

    elif fault == "Overvoltage":

        sound_file = "assets/overvoltage.mp3"

    elif fault == "Undervoltage":

        sound_file = "assets/undervoltage.mp3"

    elif fault == "Line Break":

        sound_file = "assets/emergency.mp3"

    if not sound_file:
        return

    if not os.path.exists(sound_file):

        return

    try:

        with open(
            sound_file,
            "rb",
        ) as audio_file:

            st.audio(
                audio_file.read(),
                format="audio/mp3",
                autoplay=True,
            )

    except Exception:
        pass


# ============================================================
# HISTORY SAVE
# ============================================================

def save_history(
    area_id,
    line_id,
    asset_id,
    voltage,
    current,
    frequency,
    temperature,
    fault,
    confidence,
    health,
    shutdown,
):

    initialize_history()

    try:

        history = pd.read_csv(
            history_file
        )

    except Exception:

        history = pd.DataFrame(
            columns=HISTORY_COLUMNS
        )

    new_record = pd.DataFrame(
        [
            {
                "Time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "Area": area_id,
                "Line ID": line_id,
                "Asset ID": asset_id,
                "Voltage": round(
                    float(voltage),
                    2,
                ),
                "Current": round(
                    float(current),
                    2,
                ),
                "Frequency": round(
                    float(frequency),
                    2,
                ),
                "Temperature": round(
                    float(temperature),
                    2,
                ),
                "Fault": fault,
                "Confidence": round(
                    float(confidence),
                    2,
                ),
                "Grid Health": health,
                "Shutdown": shutdown,
            }
        ]
    )

    history = pd.concat(
        [
            history,
            new_record,
        ],
        ignore_index=True,
    )

    history.to_csv(
        history_file,
        index=False,
    )


# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    try:
        show_animated_logo()
    except Exception:
        st.title("⚡ GridGuard AI")

    # --------------------------------------------------------
    # DEMO MODE
    # --------------------------------------------------------

    demo = st.toggle(
        "🎬 Presentation Demo Mode"
    )

    if demo:

        st_autorefresh(
            interval=1500,
            key="demo_refresh",
        )

    else:

        st_autorefresh(
            interval=60000,
            key="weather_refresh",
        )

    st.markdown("---")

    # --------------------------------------------------------
    # INPUT MODE
    # --------------------------------------------------------

    mode = st.radio(
        "Choose Input Mode",
        [
            "Manual Input",
            "Live Simulation",
            "⚡ Circuit Builder",
            "Virtual LT Circuit",
        ],
        horizontal=True,
    )

    # ========================================================
    # VALUES INITIALIZATION
    # ========================================================

    voltage = float(
        st.session_state.get(
            "voltage",
            230.0,
        )
    )

    current = float(
        st.session_state.get(
            "current",
            5.0,
        )
    )

    frequency = float(
        st.session_state.get(
            "frequency",
            50.0,
        )
    )

    temperature = float(
        st.session_state.get(
            "temperature",
            30.0,
        )
    )

    circuit_condition = "Normal"

    area_id = st.session_state.get(
        "last_area_id",
        "Unknown",
    )

    line_id = st.session_state.get(
        "last_line_id",
        "Unknown",
    )

    asset_id = st.session_state.get(
        "last_asset_id",
        "Unknown",
    )

    # ========================================================
    # PRESENTATION DEMO
    # ========================================================

    if demo:

        sensor = generate_demo_data()

        voltage = float(
            sensor["Voltage"]
        )

        current = float(
            sensor["Current"]
        )

        frequency = float(
            sensor["Frequency"]
        )

        temperature = float(
            sensor["Temperature"]
        )

        st.session_state["voltage"] = voltage
        st.session_state["current"] = current
        st.session_state["frequency"] = frequency
        st.session_state["temperature"] = temperature

        st.success(
            "🎬 Presentation Demo Mode Running"
        )

    # ========================================================
    # MANUAL INPUT
    # ========================================================

    elif mode == "Manual Input":

        col1, col2 = st.columns(2)

        with col1:

            voltage = st.number_input(
                "🔌 Voltage (V)",
                min_value=0.0,
                value=230.0,
                step=1.0,
            )

            current = st.number_input(
                "⚡ Current (A)",
                min_value=0.0,
                value=5.0,
                step=0.1,
            )

        with col2:

            frequency = st.number_input(
                "📡 Frequency (Hz)",
                min_value=0.0,
                value=50.0,
                step=0.1,
            )

            temperature = st.number_input(
                "🌡 Temperature (°C)",
                min_value=0.0,
                value=30.0,
                step=0.5,
            )

        st.session_state["voltage"] = voltage
        st.session_state["current"] = current
        st.session_state["frequency"] = frequency
        st.session_state["temperature"] = temperature

    # ========================================================
    # LIVE SIMULATION
    # ========================================================

    elif mode == "Live Simulation":

        sensor = generate_sensor_data()

        voltage = float(
            sensor["Voltage"]
        )

        current = float(
            sensor["Current"]
        )

        frequency = float(
            sensor["Frequency"]
        )

        temperature = float(
            sensor["Temperature"]
        )

        st.session_state["voltage"] = voltage
        st.session_state["current"] = current
        st.session_state["frequency"] = frequency
        st.session_state["temperature"] = temperature

        st.info(
            "⚡ Live Simulation Mode"
        )

    # ========================================================
    # 3-PHASE CIRCUIT BUILDER
    # ========================================================

    elif mode == "⚡ Circuit Builder":

        st.markdown(
            "## ⚡ 3-Phase LT Circuit Builder"
        )

        try:

            circuit_data = show_circuit_builder()

        except Exception as exc:

            st.error(
                "Circuit Builder could not be loaded."
            )

            st.exception(exc)

            circuit_data = {}

        # ----------------------------------------------------
        # Read asset information
        # ----------------------------------------------------

        area_id = circuit_data.get(
            "area_id",
            "Unknown",
        )

        line_id = circuit_data.get(
            "line_id",
            "Unknown",
        )

        asset_id = circuit_data.get(
            "asset_id",
            "Unknown",
        )

        st.session_state["last_area_id"] = area_id
        st.session_state["last_line_id"] = line_id
        st.session_state["last_asset_id"] = asset_id

        # ----------------------------------------------------
        # Check if circuit has simulation data
        # ----------------------------------------------------

        simulation_available = circuit_data.get(
            "simulation_available",
            False,
        )

        # ----------------------------------------------------
        # Preferred NEW circuit builder output
        # ----------------------------------------------------

        if simulation_available:

            voltage = float(
                circuit_data.get(
                    "voltage",
                    230.0,
                )
            )

            current = float(
                circuit_data.get(
                    "current",
                    5.0,
                )
            )

            frequency = float(
                circuit_data.get(
                    "sim_frequency",
                    circuit_data.get(
                        "frequency",
                        50.0,
                    ),
                )
            )

            temperature = float(
                circuit_data.get(
                    "temperature",
                    30.0,
                )
            )

            circuit_condition = circuit_data.get(
                "simulation_fault",
                "Normal",
            )

            st.session_state["voltage"] = voltage
            st.session_state["current"] = current
            st.session_state["frequency"] = frequency
            st.session_state["temperature"] = temperature

            st.markdown(
                "### 🔌 3-Phase LT Feeder Simulation Output"
            )

            st.caption(
                "Virtual circuit sensor values generated from "
                "the selected Area / Line / Asset."
            )

            st.info(
                f"""
                📍 Area: **{area_id}**  
                ⚡ Line: **{line_id}**  
                🔌 Asset: **{asset_id}**
                """
            )

            a1, a2, a3, a4 = st.columns(4)

            a1.metric(
                "📡 Voltage",
                f"{voltage:.2f} V",
            )

            a2.metric(
                "⚡ Current",
                f"{current:.2f} A",
            )

            a3.metric(
                "📡 Frequency",
                f"{frequency:.2f} Hz",
            )

            a4.metric(
                "🌡 Temperature",
                f"{temperature:.2f} °C",
            )

            if circuit_condition == "Normal":

                st.success(
                    "🟢 Virtual feeder energized — "
                    "V/I/F/T values ready for AI monitoring."
                )

            elif circuit_condition == "Line Break":

                st.error(
                    "🔴 Virtual feeder conductor fault — "
                    "supply interrupted in the simulation."
                )

            else:

                st.warning(
                    f"⚠️ Virtual feeder condition: "
                    f"{circuit_condition}"
                )

        # ----------------------------------------------------
        # Compatibility fallback
        # ----------------------------------------------------

        else:

            st.warning(
                "⚠️ Run the Virtual Circuit simulation "
                "inside the Circuit Builder to generate "
                "V/I/F/T values for AI analysis."
            )

    # ========================================================
    # OLD VIRTUAL LT CIRCUIT
    # ========================================================

    elif mode == "Virtual LT Circuit":

        st.markdown(
            "### ⚡ Virtual LT Feeder — Circuit Input"
        )

        st.info(
            "Transformer → MCB → LT Cable → "
            "Connected Loads → Virtual Sensors → GridGuard AI"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            source_voltage = st.slider(
                "⚡ Transformer Voltage (V)",
                200.0,
                250.0,
                230.0,
                1.0,
                key="vc_source_voltage",
            )

        with c2:

            line_length = st.slider(
                "📏 LT Cable Length (m)",
                50,
                500,
                100,
                10,
                key="vc_line_length",
            )

        with c3:

            wire_area = st.selectbox(
                "🧵 Cable Size (mm²)",
                [
                    6,
                    10,
                    16,
                    25,
                    35,
                ],
                index=2,
                key="vc_wire_area",
            )

        with c4:

            material = st.selectbox(
                "🔩 Cable Material",
                [
                    "Copper",
                    "Aluminium",
                ],
                index=0,
                key="vc_material",
            )

        st.markdown(
            "#### 🏠 Connected Loads"
        )

        l1, l2, l3, l4 = st.columns(4)

        with l1:

            lights = st.checkbox(
                "💡 Lighting — 300 W",
                True,
                key="vc_lights",
            )

        with l2:

            fans = st.checkbox(
                "🌀 Fans — 400 W",
                True,
                key="vc_fans",
            )

        with l3:

            refrigerator = st.checkbox(
                "❄ Refrigerator — 450 W",
                True,
                key="vc_refrigerator",
            )

        with l4:

            heavy_load = st.checkbox(
                "🏭 Heavy Load — 2500 W",
                False,
                key="vc_heavy_load",
            )

        load_power = (
            (300 if lights else 0)
            + (400 if fans else 0)
            + (450 if refrigerator else 0)
            + (2500 if heavy_load else 0)
        )

        if load_power == 0:
            load_power = 100

        line_break = st.toggle(
            "💥 Simulate LT Line Break",
            False,
            key="vc_line_break",
        )

        if line_break:

            circuit_condition = "Line Break"

        elif source_voltage < 215:

            circuit_condition = "Undervoltage"

        elif source_voltage > 245:

            circuit_condition = "Overvoltage"

        elif heavy_load:

            circuit_condition = "Overload"

        else:

            circuit_condition = "Normal"

        try:

            simulation = simulate_circuit(
                source_voltage=source_voltage,
                frequency=50.0,
                material=material,
                length_m=line_length,
                area_mm2=wire_area,
                load_power_w=load_power,
                fault=circuit_condition,
                temperature=30.0,
            )

            sensors = read_virtual_sensors(
                simulation
            )

            voltage = float(
                sensors["Voltage"]
            )

            current = float(
                sensors["Current"]
            )

            frequency = float(
                sensors["Frequency"]
            )

            temperature = float(
                sensors["Temperature"]
            )

            st.session_state["voltage"] = voltage
            st.session_state["current"] = current
            st.session_state["frequency"] = frequency
            st.session_state["temperature"] = temperature

            # ------------------------------------------------
            # Circuit visualization
            # ------------------------------------------------

            st.markdown(
                "### 🔌 Virtual LT Electrical Protection Circuit"
            )

            st.markdown(
                f"""
                <div style="
                    padding:24px;
                    border-radius:20px;
                    background:
                    linear-gradient(135deg,#0b1220,#111827);
                    border:1px solid #334155;
                    text-align:center;
                ">

                    <div style="
                        font-size:15px;
                        color:#94a3b8;
                        margin-bottom:14px;
                    ">
                        VIRTUAL SOFTWARE CIRCUIT —
                        NO PHYSICAL HARDWARE
                    </div>

                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        gap:10px;
                        flex-wrap:wrap;
                    ">

                        <div style="
                            padding:15px;
                            border-radius:14px;
                            border:2px solid #64748b;
                            min-width:125px;
                        ">
                            ⚡<br>
                            <b>AC SUPPLY</b><br>
                            <small>
                                {source_voltage:.1f} V / 50 Hz
                            </small>
                        </div>

                        <div style="font-size:26px;">
                            ━━▶
                        </div>

                        <div style="
                            padding:15px;
                            border-radius:14px;
                            border:2px solid #64748b;
                            min-width:125px;
                        ">
                            🔌<br>
                            <b>MCB</b><br>
                            <small>Protection</small>
                        </div>

                        <div style="font-size:26px;">
                            ━━▶
                        </div>

                        <div style="
                            padding:15px;
                            border-radius:14px;
                            border:2px solid #64748b;
                            min-width:145px;
                        ">
                            📏<br>
                            <b>LT LINE</b><br>
                            <small>
                                {line_length} m /
                                {material}
                            </small>
                        </div>

                        <div style="font-size:26px;">
                            ━━▶
                        </div>

                        <div style="
                            padding:15px;
                            border-radius:14px;
                            border:2px solid #64748b;
                            min-width:135px;
                        ">
                            🏠<br>
                            <b>LOAD</b><br>
                            <small>
                                {load_power} W
                            </small>
                        </div>

                    </div>

                    <div style="
                        margin:18px auto 0;
                        max-width:850px;
                        padding:15px;
                        border-radius:14px;
                        border:1px dashed #38bdf8;
                    ">

                        📡 <b>VIRTUAL SENSOR LAYER</b>
                        <br><br>

                        Voltage Sensor
                        &nbsp;│&nbsp;

                        Current Sensor
                        &nbsp;│&nbsp;

                        Frequency Sensor
                        &nbsp;│&nbsp;

                        Temperature Sensor

                    </div>

                    <div style="
                        margin-top:14px;
                        font-size:14px;
                        color:#cbd5e1;
                    ">

                        Sensor measurements →
                        <b>GridGuard AI</b> →
                        AI Fault Prediction →
                        Virtual Relay →
                        Automatic Emergency Shutdown

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            v1, v2, v3, v4 = st.columns(4)

            v1.metric(
                "📡 Voltage Sensor",
                f"{voltage:.2f} V",
            )

            v2.metric(
                "📡 Current Sensor",
                f"{current:.2f} A",
            )

            v3.metric(
                "📡 Frequency Sensor",
                f"{frequency:.2f} Hz",
            )

            v4.metric(
                "📡 Temperature Sensor",
                f"{temperature:.2f} °C",
            )

            try:

                status = get_circuit_status(
                    simulation
                )

            except Exception:

                status = circuit_condition

            if circuit_condition == "Normal":

                st.success(
                    f"🟢 Circuit Status: {status}"
                )

            elif circuit_condition == "Line Break":

                st.error(
                    f"🔴 Circuit Status: {status}"
                )

            else:

                st.warning(
                    f"⚠️ Circuit Status: {status}"
                )

            if isinstance(
                simulation,
                dict,
            ):

                resistance = simulation.get(
                    "Line Resistance",
                    "N/A",
                )

                sim_load = simulation.get(
                    "Load Power",
                    load_power,
                )

                st.caption(
                    f"Line Resistance: "
                    f"{resistance} Ω | "
                    f"Load Power: "
                    f"{sim_load} W | "
                    f"Cable: {material} "
                    f"{wire_area} mm²"
                )

        except Exception as exc:

            st.error(
                "Virtual circuit simulation failed."
            )

            st.exception(exc)

    # ========================================================
    # SAVE SENSOR VALUES
    # ========================================================

    st.session_state["voltage"] = float(
        voltage
    )

    st.session_state["current"] = float(
        current
    )

    st.session_state["frequency"] = float(
        frequency
    )

    st.session_state["temperature"] = float(
        temperature
    )

    # ========================================================
    # ASSET INFORMATION
    # ========================================================

    if mode in [
        "⚡ Circuit Builder",
    ]:

        st.markdown("---")

        st.markdown(
            f"""
            ### 📍 Active Grid Asset

            **Area:** `{area_id}`  
            **Line:** `{line_id}`  
            **Asset:** `{asset_id}`
            """
        )

    # ========================================================
    # EXECUTIVE DASHBOARD
    # ========================================================

    st.markdown("---")

    show_executive_dashboard(
        st.session_state.get(
            "fault",
            "Normal",
        ),
        st.session_state.get(
            "confidence",
            0.0,
        ),
    )

    # ========================================================
    # WEATHER
    # ========================================================

    try:

        lat = 13.0827
        lon = 80.2707

        weather = get_weather_by_coordinates(
            lat,
            lon,
        )

        if weather:

            st.markdown(
                "### 🌦 Live Weather"
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "🌡 Temperature",
                    f"{weather['temperature']} °C",
                )

            with c2:

                st.metric(
                    "💧 Humidity",
                    f"{weather['humidity']} %",
                )

            with c3:

                st.metric(
                    "💨 Wind",
                    f"{weather['wind']} m/s",
                )

            with c4:

                st.metric(
                    "☁ Weather",
                    weather["weather"],
                )

            st.caption(
                weather.get(
                    "description",
                    "",
                )
            )

    except Exception:
        pass

    # ========================================================
    # LIVE METRICS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📡 Current Virtual Sensor Values"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Voltage",
        f"{voltage:.2f} V",
    )

    c2.metric(
        "Current",
        f"{current:.2f} A",
    )

    c3.metric(
        "Frequency",
        f"{frequency:.2f} Hz",
    )

    c4.metric(
        "Temperature",
        f"{temperature:.2f} °C",
    )

    # ========================================================
    # GAUGES
    # ========================================================

    st.subheader(
        "📟 Live SCADA Gauges"
    )

    g1, g2 = st.columns(2)

    with g1:

        st.plotly_chart(
            create_gauge(
                "Voltage (V)",
                voltage,
                0,
                300,
            ),
            use_container_width=True,
        )

    with g2:

        st.plotly_chart(
            create_gauge(
                "Current (A)",
                current,
                0,
                50,
            ),
            use_container_width=True,
        )

    g3, g4 = st.columns(2)

    with g3:

        st.plotly_chart(
            create_gauge(
                "Frequency (Hz)",
                frequency,
                45,
                55,
            ),
            use_container_width=True,
        )

    with g4:

        st.plotly_chart(
            create_gauge(
                "Temperature (°C)",
                temperature,
                0,
                100,
            ),
            use_container_width=True,
        )

    # ========================================================
    # NOTIFICATIONS
    # ========================================================

    st.markdown("---")

    show_notifications(
        st.session_state.get(
            "fault",
            "Normal",
        )
    )

    # ========================================================
    # SENSOR HISTORY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📈 Live Sensor Trends"
    )

    histories = {
        "voltage_history": voltage,
        "current_history": current,
        "frequency_history": frequency,
        "temperature_history": temperature,
    }

    for key, value in histories.items():

        if key not in st.session_state:

            st.session_state[key] = []

        st.session_state[key].append(
            value
        )

        st.session_state[key] = (
            st.session_state[key][-20:]
        )

    g1, g2 = st.columns(2)

    with g1:

        st.plotly_chart(
            create_live_graph(
                st.session_state[
                    "voltage_history"
                ],
                "Voltage Trend",
                "Voltage (V)",
            ),
            use_container_width=True,
        )

    with g2:

        st.plotly_chart(
            create_live_graph(
                st.session_state[
                    "current_history"
                ],
                "Current Trend",
                "Current (A)",
            ),
            use_container_width=True,
        )

    g3, g4 = st.columns(2)

    with g3:

        st.plotly_chart(
            create_live_graph(
                st.session_state[
                    "frequency_history"
                ],
                "Frequency Trend",
                "Frequency (Hz)",
            ),
            use_container_width=True,
        )

    with g4:

        st.plotly_chart(
            create_live_graph(
                st.session_state[
                    "temperature_history"
                ],
                "Temperature Trend",
                "Temperature (°C)",
            ),
            use_container_width=True,
        )

    # ========================================================
    # AI PREDICTION
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🧠 GridGuard AI Fault Detection"
    )

    st.caption(
        "The AI prediction uses the generated V/I/F/T "
        "sensor values. The selected circuit condition "
        "is not used as the prediction result."
    )

    if model is None:

        st.error(
            "AI model is not available."
        )

        st.code(
            model_error or
            "Unknown model loading error."
        )

        fault = "Normal"
        confidence = 0.0

    else:

        try:

            fault, confidence = predict_fault(
                voltage,
                current,
                frequency,
                temperature,
            )

            st.session_state[
                "fault"
            ] = fault

            st.session_state[
                "confidence"
            ] = confidence

        except Exception as exc:

            st.error(
                "AI prediction failed."
            )

            st.exception(exc)

            fault = st.session_state.get(
                "fault",
                "Normal",
            )

            confidence = st.session_state.get(
                "confidence",
                0.0,
            )

    # ========================================================
    # GRID HEALTH + SHUTDOWN
    # ========================================================

    health, shutdown = calculate_grid_health(
        fault
    )

    st.session_state[
        "health"
    ] = health

    st.session_state[
        "shutdown"
    ] = shutdown

    # ========================================================
    # PREDICTION DISPLAY
    # ========================================================

    if fault == "Normal":

        st.success(
            f"⚡ Detected Fault: {fault}"
        )

    else:

        st.error(
            f"⚠️ Detected Fault: {fault}"
        )

    st.info(
        f"🎯 AI Confidence: "
        f"{confidence:.2f}%"
    )

    # ========================================================
    # ALARM
    # ========================================================

    show_fault_alarm(
        fault
    )

    # ========================================================
    # RESULT METRICS
    # ========================================================

    st.markdown(
        "### 🚨 Grid Protection Status"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "⚠ Fault",
        fault,
    )

    c2.metric(
        "📊 Confidence",
        f"{confidence:.2f}%",
    )

    c3.metric(
        "💚 Grid Health",
        f"{health}%",
    )

    c4.metric(
        "🚨 Shutdown",
        shutdown,
    )

    # ========================================================
    # LINE-SPECIFIC SHUTDOWN
    # ========================================================

    if shutdown == "YES":

        st.error(
            f"""
            🚨 AUTOMATIC EMERGENCY SHUTDOWN ACTIVATED

            Area: {area_id}

            Line: {line_id}

            Asset: {asset_id}

            Detected Fault: {fault}

            The virtual protection logic has isolated
            the affected grid section in the software model.
            """
        )

    else:

        st.success(
            f"""
            🟢 GRID OPERATING NORMALLY

            Line: {line_id}

            Asset: {asset_id}

            No emergency shutdown required.
            """
        )

    # ========================================================
    # SAVE HISTORY
    # ========================================================

    try:

        save_history(
            area_id=area_id,
            line_id=line_id,
            asset_id=asset_id,
            voltage=voltage,
            current=current,
            frequency=frequency,
            temperature=temperature,
            fault=fault,
            confidence=confidence,
            health=health,
            shutdown=shutdown,
        )

    except Exception as exc:

        st.warning(
            f"History could not be saved: {exc}"
        )

    # ========================================================
    # SCADA
    # ========================================================

    st.markdown("---")

    st.subheader(
        "⚡ SCADA Smart Grid"
    )

    try:

        show_scada_grid(
            fault
        )

    except Exception as exc:

        st.warning(
            f"SCADA visualization unavailable: {exc}"
        )

    # ========================================================
    # AI RECOMMENDATION
    # ========================================================

    st.markdown("---")

    st.subheader(
        "💡 AI Recommendation"
    )

    show_recommendation(
        fault
    )

    # ========================================================
    # PDF REPORT
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📄 Prediction Report"
    )

    try:

        pdf = generate_pdf(
            voltage=voltage,
            current=current,
            frequency=frequency,
            temperature=temperature,
            fault=fault,
            confidence=confidence,
            health=health,
            shutdown=shutdown,
        )

        if pdf and os.path.exists(pdf):

            with open(
                pdf,
                "rb",
            ) as file:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=file.read(),
                    file_name=os.path.basename(
                        pdf
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

    except Exception as exc:

        st.warning(
            f"PDF report could not be generated: {exc}"
        )

    # ========================================================
    # SMART GRID STATUS
    # ========================================================

    st.markdown("---")

    try:

        show_grid_status(
            fault
        )

    except Exception as exc:

        st.warning(
            f"Grid visualization unavailable: {exc}"
        )


# ============================================================
# FAULT HISTORY
# ============================================================

elif menu == "📋 Fault History":

    st.title(
        "📋 Fault History"
    )

    initialize_history()

    try:

        history = pd.read_csv(
            history_file
        )

    except Exception:

        history = pd.DataFrame(
            columns=HISTORY_COLUMNS
        )

    if history.empty:

        st.info(
            "No fault history available."
        )

    else:

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True,
        )

        csv = history.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(
            "⬇ Download History",
            csv,
            "GridGuard_History.csv",
            "text/csv",
        )


# ============================================================
# ANALYTICS
# ============================================================

elif menu == "📈 Analytics":

    st.title(
        "📈 Grid Analytics"
    )

    initialize_history()

    try:

        show_history_dashboard(
            history_file
        )

    except Exception as exc:

        st.warning(
            f"History dashboard unavailable: {exc}"
        )

    history = pd.read_csv(
        history_file
    )

    if history.empty:

        st.warning(
            "No data available."
        )

    else:

        st.subheader(
            "Voltage Trend"
        )

        fig1 = px.line(
            history,
            x="Time",
            y="Voltage",
            markers=True,
            title="Voltage vs Time",
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
        )

        st.subheader(
            "Current Trend"
        )

        fig2 = px.line(
            history,
            x="Time",
            y="Current",
            markers=True,
            title="Current vs Time",
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

        st.subheader(
            "Temperature Trend"
        )

        fig3 = px.line(
            history,
            x="Time",
            y="Temperature",
            markers=True,
            title="Temperature vs Time",
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

        st.subheader(
            "Fault Distribution"
        )

        fig4 = px.pie(
            history,
            names="Fault",
            title="Detected Faults",
        )

        st.plotly_chart(
            fig4,
            use_container_width=True,
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "📊 Project Statistics"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Predictions",
            len(history),
        )

        c2.metric(
            "Fault Types",
            history["Fault"].nunique(),
        )

        c3.metric(
            "Average Grid Health",
            f"{history['Grid Health'].mean():.1f}%",
        )


# ============================================================
# REPORTS
# ============================================================

elif menu == "📄 Reports":

    st.title(
        "📄 Reports"
    )

    initialize_history()

    history = pd.read_csv(
        history_file
    )

    if history.empty:

        st.warning(
            "No report available."
        )

    else:

        st.subheader(
            "Latest Fault Report"
        )

        latest = history.iloc[-1]

        st.write(
            f"**Time:** {latest['Time']}"
        )

        st.write(
            f"**Area:** {latest.get('Area', 'Unknown')}"
        )

        st.write(
            f"**Line ID:** {latest.get('Line ID', 'Unknown')}"
        )

        st.write(
            f"**Asset ID:** {latest.get('Asset ID', 'Unknown')}"
        )

        st.write(
            f"**Voltage:** {latest['Voltage']} V"
        )

        st.write(
            f"**Current:** {latest['Current']} A"
        )

        st.write(
            f"**Frequency:** {latest['Frequency']} Hz"
        )

        st.write(
            f"**Temperature:** {latest['Temperature']} °C"
        )

        st.write(
            f"**Fault:** {latest['Fault']}"
        )

        st.write(
            f"**Confidence:** {latest['Confidence']} %"
        )

        st.write(
            f"**Grid Health:** "
            f"{latest['Grid Health']} %"
        )

        st.write(
            f"**Shutdown:** {latest['Shutdown']}"
        )

        csv = history.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(
            "⬇ Download Complete Report",
            csv,
            "GridGuard_Report.csv",
            "text/csv",
        )


# ============================================================
# LIVE MONITORING
# ============================================================

elif menu == "📊 Live Monitoring":

    st.title(
        "📊 Live Grid Monitoring"
    )

    initialize_history()

    history = pd.read_csv(
        history_file
    )

    if history.empty:

        st.warning(
            "No sensor data available."
        )

    else:

        latest = history.iloc[-1]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🔌 Voltage",
            f"{latest['Voltage']} V",
        )

        c2.metric(
            "⚡ Current",
            f"{latest['Current']} A",
        )

        c3.metric(
            "🌡 Temperature",
            f"{latest['Temperature']} °C",
        )

        c4.metric(
            "💚 Grid Health",
            f"{latest['Grid Health']} %",
        )

        st.markdown("---")

        st.subheader(
            "Latest Fault"
        )

        if latest["Shutdown"] == "YES":

            st.error(
                f"""
                Fault: {latest['Fault']}

                Line: {latest.get('Line ID', 'Unknown')}

                Asset: {latest.get('Asset ID', 'Unknown')}

                Emergency Shutdown Activated
                """
            )

        else:

            st.success(
                "🟢 Grid Operating Normally"
            )


# ============================================================
# TAMIL NADU GIS
# ============================================================

elif menu == "🗺️ Tamil Nadu GIS":

    st.title(
        "🗺️ Tamil Nadu Grid GIS"
    )

    try:

        show_plotly_map()

    except Exception as exc:

        st.error(
            "GIS map could not be loaded."
        )

        st.exception(exc)


# ============================================================
# ABOUT
# ============================================================

elif menu == "ℹ️ About":

    st.title(
        "ℹ️ About GridGuard AI"
    )

    st.markdown(
        """
# ⚡ GridGuard AI

GridGuard AI is an Artificial Intelligence based
Low Tension (LT) power distribution fault detection
and virtual protection system.

## 🧠 AI Fault Detection

The system predicts:

- Normal
- Overload
- Overvoltage
- Undervoltage
- Line Break

using the existing machine-learning model:

`fault_model.pkl`

The model receives:

- Voltage
- Current
- Frequency
- Temperature

from the virtual sensor layer.

---

## ⚡ Virtual Electrical Architecture

```text
Grid Area
    ↓
Line
    ↓
Asset
    ↓
11 kV Supply
    ↓
Transformer
    ↓
R / Y / B / N LT Feeder
    ↓
Consumers
    ↓
Virtual V/I/F/T Sensors
    ↓
GridGuard AI
    ↓
Fault + Confidence
    ↓
Grid Health
    ↓
Virtual Relay
    ↓
Automatic Emergency Shutdown""")