import streamlit as st
import base64
import os
import time


def play_alarm(fault):

    # ----------------------------
    # Select Alarm Sound
    # ----------------------------

    sound_file = None

    if fault == "Overload":
        sound_file = "assets/overload.mp3"

    elif fault == "Overvoltage":
        sound_file = "assets/overvoltage.mp3"

    elif fault == "Undervoltage":
        sound_file = "assets/undervoltage.mp3"

    elif fault == "Frequency Fault":
        sound_file = "assets/frequency.mp3"


    # ----------------------------
    # Play Alarm
    # ----------------------------

    if sound_file and os.path.exists(sound_file):

        with open(sound_file, "rb") as audio_file:
            audio_bytes = audio_file.read()

        audio_base64 = base64.b64encode(audio_bytes).decode()

        unique_id = str(time.time())

        audio_html = f"""
        <audio id="alarm_{unique_id}" autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """

        st.markdown(audio_html, unsafe_allow_html=True)

    else:
        st.warning(f"⚠ Alarm file missing: {sound_file}")