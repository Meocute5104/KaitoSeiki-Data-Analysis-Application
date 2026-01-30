import plotly.express as px

def process_bar(df, processes, std_total, title):
    fig = px.bar(df, x="SP", y=processes, title=title)
    fig.add_hline(y=std_total, line_dash="dash", line_color="red", annotation_text="標準工数")
    fig.update_xaxes(type="category")
    return fig
