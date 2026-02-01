import plotly.express as px

def efficiency_heatmap(df, processes, title): 
    #df contains 'SP' and process columns, processes is a list of process column names, title is a string, returns a heatmap figure
    fig = px.imshow(
        df.set_index("SP")[processes],
        text_auto=True,
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=100,
        range_color=[50, 150],
        aspect="auto",
        title=title
    )
    fig.update_yaxes(type="category")
    return fig
