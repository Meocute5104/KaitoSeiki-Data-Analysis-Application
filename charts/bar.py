import plotly.express as px

def process_bar(df, processes, std_total, title): 
    avg_act = df["totalTime"].mean()
    #df contains 'SP' and process columns, std_total is a numeric value, title is a string, returns a bar chart with a horizontal line
    #fix là vẽ biểu đồ thanh với các tiến trình trên trục y và SP trên trục x, thêm một đường ngang biểu thị std_total

    fig = px.bar(df, x="SP", y=processes, title=title)
    fig.add_hline(y=std_total,line_dash="dash",line_color="red")
    fig.add_hline(y=avg_act,line_dash="dot",line_color="blue")

    fig.add_annotation(
        x=1.01,
        y=std_total,
        xref="paper",
        yref="y",
        text="標準工数",
        showarrow=False,
        font=dict(color="red")
    )

    fig.add_annotation(
        x=1.01,
        y=avg_act,
        xref="paper",
        yref="y",
        text="平均工数",
        showarrow=False,
        font=dict(color="blue")
    )
    # fig.add_hline(y=std_total, line_dash="dash", line_color="red", annotation_text="標準工数", annotation_position="top right", annotation_y=std_annot_y)
    # fig.add_hline(y=avg_act, line_dash="dot", line_color="blue", annotation_text="平均工数", annotation_position="bottom right", annotation_y=avg_annot_y)
    fig.update_xaxes(type="category") # Đặt trục x là loại để hiển thị tất cả các SP
    return fig
