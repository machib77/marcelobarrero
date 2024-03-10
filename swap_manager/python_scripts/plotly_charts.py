import plotly.graph_objs as go


def scatter_plot(x, y, title, mode="lines+markers"):
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
        title={
            "text": f"<b>{title}</b>",
            "x": 0.5,  # Center the title
            "xanchor": "center",
            "font": {
                "color": "white",
                "size": 18,
                "family": "Arial, sans-serif",
            },
        },
        plot_bgcolor="#212121",
        paper_bgcolor="#141414",
        font=dict(color="white"),
        xaxis=dict(color="white", gridcolor="#2e2e2e"),
        yaxis=dict(color="white", gridcolor="#2e2e2e"),
        margin=dict(l=50, r=50, t=50, b=50),
        autosize=True,
    )

    fig = go.Figure(data=data, layout=layout)
    chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return chart
