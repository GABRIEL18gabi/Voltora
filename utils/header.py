import streamlit as st
import base64


def show_animated_logo():

    with open("assets/logo.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>

        @keyframes pulse {{
            0% {{
                transform: scale(1);
                filter: drop-shadow(0 0 5px cyan);
            }}

            50% {{
                transform: scale(1.08);
                filter: drop-shadow(0 0 25px cyan);
            }}

            100% {{
                transform: scale(1);
                filter: drop-shadow(0 0 5px cyan);
            }}
        }}

        .logo {{
            display:flex;
            justify-content:center;
            margin-top:10px;
            margin-bottom:20px;
        }}

        .logo img {{
            width:170px;
            animation:pulse 2s infinite;
        }}

        </style>

        <div class="logo">
            <img src="data:image/png;base64,{encoded}">
        </div>
        """,
        unsafe_allow_html=True
    )