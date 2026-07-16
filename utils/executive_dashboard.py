import streamlit as st


def show_executive_dashboard(fault, confidence):

    health = st.session_state.get("grid_health", 96)

    power = "ONLINE" if fault == "Normal" else "SHUTDOWN"

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⚡ Grid Health", f"{health}%")
        st.metric("🚨 Fault", fault)

    with c2:
        st.metric("🔌 Power", power)
        st.metric("🤖 AI Confidence", f"{confidence:.1f}%")

    with c3:
        st.metric("🌍 Cities", 10)
        st.metric("🛰 Sensors", 125)

    st.markdown("---")