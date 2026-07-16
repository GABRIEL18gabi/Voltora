import plotly.graph_objects as go
import streamlit as st
from utils.fault_visualization import get_fault_connection


def add_power_flow(fig, df, connections, frame=0):
    fault = st.session_state.get("fault", "Normal")
    fault_connection = get_fault_connection(fault)

    for city1, city2 in connections:
        if fault_connection == (city1, city2):
            continue

        p1 = df[df["City"] == city1].iloc[0]
        p2 = df[df["City"] == city2].iloc[0]

    
        steps = 20

        index = frame % steps

        lat = (
            p1["latitude"] +
            (p2["latitude"] - p1["latitude"]) * index / steps
        )

        lon = (
            p1["longitude"] +
            (p2["longitude"] - p1["longitude"]) * index / steps
        )

        fig.add_trace(
            go.Scattermap(
                lat=[lat],
                lon=[lon],
                mode="markers",
                marker=dict(
                    size=12,
                    color="cyan"
                ),
                name="Power Flow",
                showlegend=False
            )
        )


    return fig