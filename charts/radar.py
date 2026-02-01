import plotly.graph_objects as go

def radar(processes, actual_pct):
    # processes is a list of process names, actual_pct is a list of actual percentages, returns a radar chart figure
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=actual_pct + [actual_pct[0]],
        theta=processes + [processes[0]],
        fill="toself",
        name="実際 (%)"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[100]*(len(processes)+1),
        theta=processes + [processes[0]],
        line=dict(dash="dash"),
        name="標準 (100%)", marker_color="#C42828"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, max(actual_pct+[150])])),
        title="工程比率 (%)"
    )
    return fig
