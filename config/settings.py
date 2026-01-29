import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Production Dashboard Pro",
        layout="wide"
    )

def render_title():
    st.markdown("""
    <div style="text-align:center;margin-bottom:20px">
        <h1 style="color:#1f4e78;border-bottom:3px solid #1f4e78;
        display:inline-block;padding-bottom:10px">
            🏭 インテリジェント製造分析システム
        </h1>
    </div>
    """, unsafe_allow_html=True)
