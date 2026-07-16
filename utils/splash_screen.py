import streamlit as st
import time

def startup_animation():

    placeholder = st.empty()

    placeholder.info("⚡ Initializing Smart Grid...")

    time.sleep(4)

    placeholder.empty()

    st.rerun()