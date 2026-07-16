import streamlit as st


def show_alarm_panel(fault):

    if fault == "Normal":

        st.success(
            "🟢 GRID STATUS : NORMAL"
        )

    elif fault == "Overload":

        st.warning(
            """
🚨 OVERLOAD DETECTED

⚡ Automatic Emergency Shutdown Activated

AI Recommendation:
Reduce feeder load immediately.
            """
        )

    elif fault == "Overvoltage":

        st.error(
            """
⚠ OVERVOLTAGE DETECTED

Emergency Shutdown Activated

Disconnect vulnerable equipment.
            """
        )

    elif fault == "Undervoltage":

        st.warning(
            """
⚠ UNDERVOLTAGE DETECTED

Monitor supply and restore normal voltage.
            """
        )

    elif fault == "Line Break":

        st.error(
            """
🚨 LINE BREAK DETECTED

⛔ Automatic Emergency Shutdown Activated

⚡ AI has isolated the damaged feeder.
            """
        )