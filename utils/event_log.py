import streamlit as st
from datetime import datetime
import random


def show_event_log():

    st.subheader("📜 Live SCADA Event Log")

    events = [
        "⚡ Voltage within safe limit",
        "🟢 Grid operating normally",
        "🌧 Heavy rain warning received",
        "🚨 Fault detected in feeder",
        "🔌 Emergency shutdown activated",
        "🤖 AI recommendation generated",
        "⚙ Transformer load balanced",
        "📡 Sensor data updated",
        "⚡ Backup feeder activated",
        "🛰 Disaster data synchronized"
    ]

    for _ in range(6):

        st.info(
            f"{datetime.now().strftime('%H:%M:%S')}   "
            f"{random.choice(events)}"
        )