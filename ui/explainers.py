import streamlit as st

def boxplot_help():
    with st.expander("💡 箱ひげ図の見方"):
        st.write("""
                - 中央線：中央値  
                - 箱の長さ：ばらつき  
                - 点：個別製品（外れ値）
                """)


def stack_bar_help(df, std):
    std_total = sum(std.values()) # Tổng thời gian tiêu chuẩn cho SPC hiện tại
    avg_act = df["totalTime"].mean()  # Trung bình thời gian thực tế cho SPC hiện tại
    eff_val = (std_total / avg_act) * 100  # Hiệu suất cho SPC hiện tại 
    with st.expander("📌 時間のパラメータ", expanded=True):
        st.write(f"- **標準時間（分）:** {std_total}")
        st.write(f"- **実際の平均（分）:** {avg_act:.1f}")
        color = "green" if eff_val >= 100 else "red"
        st.markdown(f"- **平均効率:** :{color}[{eff_val:.1f}%]")

def heatmap_help(df_spc, std, eff_df, processes):
    std_total = sum(std.values()) # Tổng thời gian tiêu chuẩn cho SPC đã chọn
    with st.expander("📊 効率と弱点の説明", expanded=True):
        avg_eff_per_proc = eff_df[processes].mean()

        # Chỉ lấy các process có hiệu suất < 100%
        low_eff_proc = avg_eff_per_proc[avg_eff_per_proc < 100]

        if low_eff_proc.empty:
            st.success("✅ すべての工程は平均100%以上です。")
        else:
            bottleneck_proc = low_eff_proc.idxmin()
            bottleneck_val = low_eff_proc.min()

            st.error(
                f"⚠️ **ボトルネック工程:** {bottleneck_proc} "
                f"({bottleneck_val:.1f}%)"
            )
        critical_proc = avg_eff_per_proc[avg_eff_per_proc < 90]
        for proc, val in low_eff_proc.sort_values().items():
            st.write(f"- {proc}: {val:.1f}%")

        # 1️⃣ Lọc các sản phẩm có tổng thời gian lớn hơn tiêu chuẩn
        # ================================
        # ⏱ 工数による製品比較
        # ================================

        col_slow, col_fast = st.columns(2)

        # ---------- SP CHẬM ----------
        with col_slow:
            st.markdown(
                """
                <h6 style="color:#d9534f; margin-bottom:0.3rem;">
                    標準超過
                </h6>
                """,
                unsafe_allow_html=True
            )

            slow_sp_df = df_spc.loc[
                df_spc["totalTime"] > std_total,
                ["SP", "totalTime"]
            ]

            if slow_sp_df.empty:
                st.success("標準工数を超える製品はありません。")
            else:
                top_slow_sp_df = (
                    slow_sp_df
                    .sort_values("totalTime", ascending=False)
                    .head(3)
                )

                for _, row in top_slow_sp_df.iterrows():
                    st.markdown(
                        f"""
                        <div style="
                            padding:6px 10px;
                            margin-bottom:6px;
                            border-left:4px solid #d9534f;
                            background-color:#fff5f5;
                            border-radius:6px;
                        ">
                            <span style="color:#d9534f; font-weight:600;">
                               <b>機号:</b> {row['SP']}
                            </span>
                            <span style="color:#d9534f;float:right;">
                                {row['totalTime']:.1f} 分
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # ---------- SP NHANH ----------
        with col_fast:
            st.markdown(
                """
                <h6 style="color:#5cb85c; margin-bottom:0.3rem;">
                    優秀事例
                </h6>
                """,
                unsafe_allow_html=True
            )
            fast_sp_df = df_spc.loc[
                df_spc["totalTime"] < std_total,
                ["SP", "totalTime"]
            ]

            if fast_sp_df.empty:
                st.info("標準工数より短い製品はありません。")
            else:
                top_fast_sp_df = (
                    fast_sp_df
                    .sort_values("totalTime", ascending=True)
                    .head(3)
                )

                for _, row in top_fast_sp_df.iterrows():
                    st.markdown(
                        f"""
                        <div style="
                            padding:6px 10px;
                            margin-bottom:6px;
                            border-left:4px solid #5cb85c;
                            background-color:#f5fff7;
                            border-radius:6px;
                        ">
                            <span style="color:#5cb85c; font-weight:600;">
                               <b>機号:</b> {row['SP']}
                            </span>
                            <span style="color:#5cb85c;float:right;">
                                {row['totalTime']:.1f} 分
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
