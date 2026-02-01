import plotly.graph_objects as go

def compare_bar(processes, actual, standard): 
    # processes is a list of process names, actual and standard are lists of numeric values, returns a grouped bar chart figure
    fig = go.Figure([
        go.Bar(name="実際", x=processes, y=actual),
        go.Bar(name="標準", x=processes, y=standard, marker_color='#C42828')
    ])
    fig.update_layout(barmode="group", title="実際 vs 標準 (分)")
    return fig
