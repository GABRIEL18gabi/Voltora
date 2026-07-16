import streamlit as st


def show_scada_panel(status, fault):

    st.markdown("## 🖥️ Grid Control Center")

    power = "ONLINE" if fault == "Normal" else "SHUTDOWN"

    ai = "ACTIVE"

    communication = "NORMAL"

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "⚡ Grid Health",
            f"{status['Grid Health']}%"
        )

        st.metric(
            "🚨 Active Faults",
            status["Faults"]
        )

        st.metric(
            "🤖 AI Engine",
            ai
        )

    with c2:

        st.metric(
            "🔌 Power",
            power
        )

        st.metric(
            "🌐 Communication",
            communication
        )

        st.metric(
            "⚠ Risk",
            status["Risk"]
        )

    st.markdown("---")

    if fault == "Normal":

        st.success("🟢 GRID OPERATING NORMALLY")

    else:

        st.error(f"🚨 {fault} DETECTED")

        st.warning("⚡ Emergency Shutdown Active")