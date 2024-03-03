import plotly.graph_objs as go


def scatter_plot(x, y, mode="lines+markers"):
    data = [
        go.Scatter(
            x=x,
            y=y,
            mode=mode,
        )
    ]

    layout = go.Layout()
    fig = go.Figure(data=data, layout=layout)
    chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return chart
