import plotly.graph_objects as go


def create_live_graph(data, title, yaxis_title):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=data,
            mode="lines+markers",
            name=title
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Reading",
        yaxis_title=yaxis_title,
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig