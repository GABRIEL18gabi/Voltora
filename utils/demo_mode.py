import random
import streamlit as st


def generate_demo_data():

    # First time initialization
    if "demo_voltage" not in st.session_state:

        st.session_state.demo_voltage = 230
        st.session_state.demo_current = 5
        st.session_state.demo_frequency = 50
        st.session_state.demo_temperature = 30

        st.session_state.demo_counter = 0

    # Increase counter every refresh
    st.session_state.demo_counter += 1

    # Smooth sensor movement
    st.session_state.demo_voltage += random.uniform(-2, 2)
    st.session_state.demo_current += random.uniform(-0.3, 0.3)
    st.session_state.demo_frequency += random.uniform(-0.08, 0.08)
    st.session_state.demo_temperature += random.uniform(-0.5, 0.5)

    # Safe operating limits
    st.session_state.demo_voltage = max(
        180,
        min(280, st.session_state.demo_voltage)
    )

    st.session_state.demo_current = max(
        2,
        min(18, st.session_state.demo_current)
    )

    st.session_state.demo_frequency = max(
        48,
        min(52, st.session_state.demo_frequency)
    )

    st.session_state.demo_temperature = max(
        20,
        min(70, st.session_state.demo_temperature)
    )

    # Every 15 refreshes (~15 sec)
    cycle = (st.session_state.demo_counter // 15) % 5

    if cycle == 0:

        fault = "Normal"

        confidence = 99

        health = 100

        shutdown = "NO"

    elif cycle == 1:

        fault = "Overload"

        confidence = 97

        health = 45

        shutdown = "YES"

        st.session_state.demo_current += 6

    elif cycle == 2:

        fault = "Overvoltage"

        confidence = 98

        health = 40

        shutdown = "YES"

        st.session_state.demo_voltage += 35

    elif cycle == 3:

        fault = "Undervoltage"

        confidence = 96

        health = 50

        shutdown = "YES"

        st.session_state.demo_voltage -= 35

    else:

        fault = "Line Break"

        confidence = 99

        health = 20

        shutdown = "YES"

        st.session_state.demo_current = 0

    return {

        "Voltage": round(st.session_state.demo_voltage, 1),

        "Current": round(st.session_state.demo_current, 2),

        "Frequency": round(st.session_state.demo_frequency, 2),

        "Temperature": round(st.session_state.demo_temperature, 1),

        "Fault": fault,

        "Confidence": confidence,

        "Health": health,

        "Shutdown": shutdown

    }