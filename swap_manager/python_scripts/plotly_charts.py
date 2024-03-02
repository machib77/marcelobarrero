import plotly.graph_objs as go


def scatter_plot(x, y):
    data = [
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
        )
    ]

    layout = go.Layout()
    fig = go.Figure(data=data, layout=layout)
    chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return chart
