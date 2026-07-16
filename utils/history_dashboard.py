import streamlit as st
import pandas as pd
import plotly.express as px


def show_history_dashboard(history_file):

    st.subheader("📊 Fault History Dashboard")

    history = pd.read_csv(history_file)

    if history.empty:
        st.info("No prediction history available.")
        return

    # -----------------------
    # Summary Cards
    # -----------------------
    total = len(history)
    normal = len(history[history["Fault"] == "Normal"])
    overload = len(history[history["Fault"] == "Overload"])
    overvoltage = len(history[history["Fault"] == "Overvoltage"])
    undervoltage = len(history[history["Fault"] == "Undervoltage"])

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total", total)
    c2.metric("Normal", normal)
    c3.metric("Overload", overload)
    c4.metric("Overvoltage", overvoltage)
    c5.metric("Undervoltage", undervoltage)

    st.markdown("---")

    # -----------------------
    # Pie Chart
    # -----------------------
    fig = px.pie(
        history,
        names="Fault",
        title="Fault Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    