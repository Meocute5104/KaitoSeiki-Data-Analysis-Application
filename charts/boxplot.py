import plotly.express as px

def process_boxplot(df, processes, spc): 
    #df contains 'SP', 'SPC', and process columns, processes is a list of process column names, spc is a string, returns a boxplot figure
    melted = df.melt(
        id_vars=["SP", "SPC"],
        value_vars=processes,
        var_name="工程",
        value_name="時間（分）"
    )

    fig = px.box(
        melted,
        x="工程",
        y="時間（分）",
        color="工程",
        points="all",
        hover_data=["SP"],
        title=f"工程分布ボックスプロット - {spc}"
    )
    fig.update_layout(showlegend=False)
    return fig
