import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.weather_api import get_weather_by_coordinates


def show_tamilnadu_map():

    st.title("🗺️ Tamil Nadu Disaster Intelligence Center")

    df = pd.read_csv("data/tamilnadu_cities.csv")

    # Center Tamil Nadu
    m = folium.Map(
        location=[11.1271, 78.6569],
        zoom_start=7,
        tiles="OpenStreetMap"
    )

    colors = {
        "Safe": "green",
        "Flood": "blue",
        "Cyclone": "red",
        "Heatwave": "orange",
        "Heavy Rain": "purple",
        "Unknown": "gray"
    }

    # =====================================
    # Live Weather + Markers
    # =====================================

    for _, row in df.iterrows():

        weather = get_weather_by_coordinates(
        row["latitude"],
        row["longitude"]
)

        if weather:

            if weather["wind"] >= 20:
                risk = "Cyclone"

            elif weather["temperature"] >= 40:
                risk = "Heatwave"

            elif weather["weather"] in ["Rain", "Drizzle", "Thunderstorm"]:
                risk = "Flood"

            else:
                risk = "Safe"

            popup = f"""
            <h4>{row['City']}</h4>

            🌡 Temperature : {weather['temperature']} °C<br>

            💧 Humidity : {weather['humidity']} %<br>

            💨 Wind : {weather['wind']} m/s<br>

            ☁ Weather : {weather['weather']}<br>

            ⚠ Risk : {risk}<br>

            ⚡ Grid : {row['GridStatus']}
            """

        else:

            risk = "Unknown"

            popup = f"""
            <h4>{row['City']}</h4>

            Weather Unavailable
            """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            tooltip=row["City"],
            icon=folium.Icon(
                color=colors.get(risk, "gray"),
                icon="cloud"
            )
        ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=650
    )

    st.markdown("---")

    st.subheader("📋 Tamil Nadu Cities")

    st.dataframe(df, use_container_width=True)