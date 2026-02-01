import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data(file):
    # Đọc dữ liệu thô để lấy tên cột
    df_raw = pd.read_excel(file, sheet_name="Data", nrows=0)

    # Lấy danh sách các quy trình, loại trừ các cột không cần thiết
    exclude_cols = ["SP", "SPC"]

    # Lấy danh sách các quy trình
    processes = [c for c in df_raw.columns if c not in exclude_cols]

    # Đọc dữ liệu chính với kiểu dữ liệu phù hợp
    df = pd.read_excel(file, sheet_name="Data", dtype={"SP": str, "SPC": str})
    
    # Tính tổng thời gian cho mỗi hàng
    df["totalTime"] = df[processes].sum(axis=1)

    # Lấy danh sách SPC duy nhất
    spc_list = df["SPC"].unique().tolist()

    # Đọc dữ liệu tiêu chuẩn và lọc theo danh sách SPC
    std_df = pd.read_excel(file, sheet_name="Standard", dtype={"SPC": str})
    
    # Lọc dữ liệu tiêu chuẩn theo danh sách SPC
    std_df = std_df[std_df["SPC"].isin(spc_list)]

    # Tạo bản đồ tiêu chuẩn cho mỗi SPC
    std_map = std_df.set_index("SPC")[processes].to_dict("index")

    return df, std_map, processes # Trả về DataFrame chính, bản đồ tiêu chuẩn và danh sách quy trình
