import streamlit as st
import time

def startup_animation():
    msg = st.empty()

    msg.info("⚡ Initializing Smart Grid...")

    time.sleep(4)

    msg.empty()