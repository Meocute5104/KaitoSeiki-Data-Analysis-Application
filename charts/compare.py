import plotly.graph_objects as go

def compare_bar(processes, actual, standard):
    fig = go.Figure([
        go.Bar(name="実際", x=processes, y=actual),
        go.Bar(name="標準", x=processes, y=standard, marker_color='#C42828')
    ])
    fig.update_layout(barmode="group", title="実際 vs 標準 (分)")
    return fig
