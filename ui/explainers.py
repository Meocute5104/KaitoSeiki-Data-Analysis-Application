import streamlit as st

def boxplot_help():
    with st.expander("💡 箱ひげ図の見方"):
        st.write("""
                - 中央線：中央値  
                - 箱の長さ：ばらつき  
                - 点：個別製品（外れ値）
                """)
