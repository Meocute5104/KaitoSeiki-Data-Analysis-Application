import streamlit as st

def upload():
    st.sidebar.header("📥 データをアップロード")
    return st.sidebar.file_uploader(
        " Excelファイルを選択してください（シート：Data & Standard）",
        type=["xlsx", "csv", "xls"]
    )

def select_spc(std_map):
    return st.sidebar.selectbox(
        "1. 製品タイプ (SPC)",
        ["すべて"] + sorted(std_map.keys())
    )

def select_product(df):
    return st.sidebar.selectbox(
        "2. 番号機械",
        sorted(df["SP"].unique())
    )
