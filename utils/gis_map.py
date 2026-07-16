import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


def show_gis_map():

    st.subheader("🗺️ GIS Disaster Risk Map")

    # Read CSV
    df = pd.read_csv("data/disaster_zones.csv")

    # Create map centered on the average location
    m = folium.Map(
        location=[
            df["latitude"].mean(),
            df["longitude"].mean()
        ],
        zoom_start=14,
        tiles="OpenStreetMap"
    )

    # Marker colors based on disaster risk
    colors = {
        "Safe": "green",
        "Flood": "blue",
        "Cyclone": "orange",
        "Landslide": "red"
    }

    # Add markers
    for _, row in df.iterrows():

        popup = f"""
     <b>📍 Location:</b> {row['Location']}<br>
     <b>🌍 Disaster Zone:</b> {row['Risk']}<br>
     <b>⚡ Fault:</b> {row['Fault']}<br>
     <b>🚦 Status:</b> {row['Status']}
     """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            tooltip=row["Location"],
            icon=folium.Icon(
                color=colors.get(row["Risk"], "gray"),
                icon="info-sign"
            )
        ).add_to(m)

    # Display map
    st_folium(
        m,
        width=1000,
        height=600
    )

    st.markdown("---")

    st.subheader("📋 Disaster Zone Details")

    st.dataframe(df, use_container_width=True)