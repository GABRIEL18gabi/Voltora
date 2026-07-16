import plotly.graph_objects as go


def create_gauge(title, value, min_value, max_value):
    """
    Creates a professional SCADA gauge.
    """

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,

            title={"text": title},

            gauge={
                "axis": {"range": [min_value, max_value]},

                "bar": {"color": "#1E90FF"},

                "steps": [
                    {"range": [min_value, max_value * 0.6], "color": "#90EE90"},
                    {"range": [max_value * 0.6, max_value * 0.85], "color": "#FFD700"},
                    {"range": [max_value * 0.85, max_value], "color": "#FF6347"}
                ]
            }
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

if __name__ == "__main__":
    print("SCADA Gauge Module Loaded Successfully")