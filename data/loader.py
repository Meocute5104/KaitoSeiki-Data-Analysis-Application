import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data(file):
    df_raw = pd.read_excel(file, sheet_name="Data", nrows=0)

    exclude_cols = ["SP", "SPC"]
    processes = [c for c in df_raw.columns if c not in exclude_cols]

    df = pd.read_excel(file, sheet_name="Data", dtype={"SP": str, "SPC": str})
    df["totalTime"] = df[processes].sum(axis=1)

    spc_list = df["SPC"].unique().tolist()
    std_df = pd.read_excel(file, sheet_name="Standard", dtype={"SPC": str})
    std_df = std_df[std_df["SPC"].isin(spc_list)]

    std_map = std_df.set_index("SPC")[processes].to_dict("index")
    return df, std_map, processes
