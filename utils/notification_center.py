import streamlit as st
from datetime import datetime


def show_notifications(fault):

    st.markdown("## 🔔 Notification Center")

    now = datetime.now().strftime("%H:%M:%S")

    if fault == "Normal":

        st.success(f"{now}  🟢 Grid Operating Normally")

    elif fault == "Overload":

        st.warning(f"{now}  ⚠ Overload Detected")
        st.error(f"{now}  🚨 Emergency Shutdown Activated")

    elif fault == "Overvoltage":

        st.warning(f"{now}  ⚡ Overvoltage Detected")
        st.error(f"{now}  🚨 Shutdown Activated")

    elif fault == "Undervoltage":

        st.warning(f"{now}  🔋 Undervoltage Detected")

    elif fault == "Line Break":

        st.error(f"{now}  🚨 Line Break Detected")
        st.info(f"{now}  🤖 AI Isolating Feeder")
        st.warning(f"{now}  ⚡ Backup Power Activated")