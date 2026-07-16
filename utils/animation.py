import streamlit as st
import time


def show_grid_status(fault):

    st.subheader("⚡ Smart Electrical Grid")

    # -------------------------------
    # Normal
    # -------------------------------
    if fault == "Normal":

        st.success("🟢 Grid Operating Normally")

        placeholder = st.empty()

        frames = [

"""
🏭 Transformer
      │
⚡══════⚡══════⚡
      │
⚡ Pole 1
      │
🏠🏠🏠 Houses Receiving Power
""",

"""
🏭 Transformer
      │
══════⚡══════⚡
      │
⚡ Pole 1
      │
🏠🏠🏠 Houses Receiving Power
""",

"""
🏭 Transformer
      │
⚡════════════⚡
      │
⚡ Pole 1
      │
🏠🏠🏠 Houses Receiving Power
"""
        ]

        for frame in frames:
            placeholder.markdown(f"```text\n{frame}\n```")
            time.sleep(0.4)

    # -------------------------------
    # Line Break
    # -------------------------------
    elif fault == "Line Break":

        st.error("❌ Line Break Detected")

        st.markdown("""
🏭 Transformer
      │
🟢══════════════❌══════════════🔴
      │
Pole 1     Pole 2     Pole 3
               ❌
Houses Without Power
""")

    # -------------------------------
    # Overload
    # -------------------------------
    elif fault == "Overload":

        st.error("🔥 Transformer Overload")

        st.markdown("""
🏭 Transformer
      🔥
      │
🟠══════════════════════🟠
      │
⚡ Pole 1
      │
🟠══════════════════════🟠
      │
⚡ Pole 2
      │
🟠══════════════════════🟠
      │
⚡ Pole 3
      │
🏠🏠🏠 Houses Receiving Power

⚠ High Current Flow
""")

    # -------------------------------
    # Overvoltage
    # -------------------------------
    elif fault == "Overvoltage":

        st.warning("⚡ Overvoltage Detected")

        st.markdown("""
🏭 Transformer
      ⚡
      │
🟡══════════════════════🟡
      │
⚡ Pole 1
      │
🟡══════════════════════🟡
      │
⚡ Pole 2
      │
🟡══════════════════════🟡
      │
⚡ Pole 3
      │
🏠🏠🏠 Houses Receiving Power

⚠ Voltage Above Safe Limit
""")

    # -------------------------------
    # Undervoltage
    # -------------------------------
    elif fault == "Undervoltage":

        st.warning("🔋 Undervoltage Detected")

        st.markdown("""
🏭 Transformer
      🔋
      │
🟡══════════════════════🟡
      │
⚡ Pole 1
      │
🟡══════════════════════🟡
      │
⚡ Pole 2
      │
🟡══════════════════════🟡
      │
⚡ Pole 3
      │
🏠🏠🏠 Houses Receiving Power

⚠ Voltage Below Safe Limit
""")

    # -------------------------------
    # Unknown Fault
    # -------------------------------
    else:

        st.error("🚨 Unknown Fault Detected")

        st.markdown("""
🏭 Transformer
      │
🔴══════════════❌══════════════🔴
      │
Grid Fault

Power Supply Interrupted
""")


if __name__ == "__main__":
    print("Animation Module Loaded Successfully")