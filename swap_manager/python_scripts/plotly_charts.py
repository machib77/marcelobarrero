import plotly.graph_objs as go


def scatter_plot(x, y, mode="lines+markers"):
    data = [
        go.Scatter(
            x=x,
            y=y,
            mode=mode,
            line=dict(color="#ff9c29", width=1),
            marker=dict(color="#ff9c29", size=6),
        )
    ]

    layout = go.Layout(
        plot_bgcolor="#212121",
        paper_bgcolor="#141414",
        font=dict(color="white"),
        xaxis=dict(color="white", gridcolor="#2e2e2e"),
        yaxis=dict(color="white", gridcolor="#2e2e2e"),
    )
    fig = go.Figure(data=data, layout=layout)
    chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return chart
