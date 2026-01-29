import pandas as pd
import streamlit as st
from config.settings import setup_page, render_title
from data.loader import load_data
from ui.sidebar import upload, select_spc, select_product
from services.metrics import efficiency, bottleneck, worst_product
from charts.bar import process_bar
from charts.heatmap import efficiency_heatmap
from charts.boxplot import process_boxplot
from charts.radar import radar
from charts.compare import compare_bar
from ui.explainers import boxplot_help

setup_page()
render_title()

uploaded = upload()

if not uploaded:
    st.info("👋 ようこそ！Excelファイルをアップロードして分析を開始してください")
    st.stop()

if uploaded is not None:
    with st.spinner("⏳ データを処理中..."):
        try:
            # Gọi hàm đã được cache
            df, std_map, processes = load_data(uploaded)
            selected_spc = select_spc(std_map)
            
            st.sidebar.success("✅ データが正常にアップロードされました！")
            
            if selected_spc == "すべて":
                st.markdown('<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">📈 全製品のSPC分析</h2>', unsafe_allow_html=True)                
                st.write("各SPCごとの詳細な分析を以下に示します。")
                # Hiển thị dữ liệu gốc
                with st.expander("📊 元データ"):
                    # df la tat ca du lieu khi chon 'Tat ca'
                    st.dataframe(df, use_container_width=True)
                
                for spc, std in std_map.items():
                    df_spc = df[df["SPC"] == spc]
                    if df_spc.empty:
                        continue

                    std_total = sum(std.values())
                    avg = df_spc["totalTime"].mean()
                    eff = efficiency(std_total, avg)
                    avg_act = df_spc["totalTime"].mean()
                    eff_val = efficiency(std_total, avg_act)

                    eff_df = df_spc.copy()
                    for p in processes:
                        eff_df[p] = (std[p] / eff_df[p] * 100).round(1)

                    st.markdown(f"""<h3 style="color: #1f4e78; border-bottom: 2px solid #1f4e78; width: fit-content; padding-bottom: 5px;">
                                    SPC: {spc}
                                </h3>""", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            process_bar(df_spc, processes, std_total, f"進程の分布 - {spc} "),
                            use_container_width=True
                        )
                        with st.expander("📌 時間のパラメータ", expanded=True):
                            st.write(f"**標準時間（分）:** {std_total}")
                            st.write(f"**実際の平均（分）:** {avg_act:.1f}")
                            color = "green" if eff_val >= 100 else "red"
                            st.markdown(f"**効率:** :{color}[{eff_val:.1f}%]")

                    with col2:
                        st.plotly_chart(
                            efficiency_heatmap(eff_df, processes, f"ヒートマップ効率 (%) - {spc}"),
                            use_container_width=True
                        )
                        with st.expander("📊 効率と弱点の説明", expanded=True):
                            # Tìm tiến trình chậm nhất (Bottleneck)
                            avg_eff_per_proc = eff_df[processes].mean()
                            bottleneck_proc = avg_eff_per_proc.idxmin()
                            bottleneck_val = avg_eff_per_proc.min()
                            
                            # Tính hiệu suất tổng dựa trên các biến đã định nghĩa trước đó
                            # Lưu ý: Đảm bảo std_total và avg_actual_total đã được tính ở đoạn code phía trên
                            eff_total = (std_total / avg_act) * 100
                            
                            # Tìm sản phẩm yếu nhất - Cần dùng đúng set_index('SP')
                            worst_prod = eff_df.set_index('SP')[processes].mean(axis=1).idxmin()
                                
                            st.write(f"**平均効率:** {eff_total:.1f}%")
                            st.write(f"**ボトルネック:** {bottleneck_proc} ({bottleneck_val:.1f}%)")
                            
                            # worst_prod lúc này sẽ là String (ví dụ: '01191744') nhờ bước ép kiểu lúc read_excel
                            st.markdown(f"**注意製品:** :red[{worst_prod}]")

                    st.plotly_chart(
                        process_boxplot(df_spc, processes, spc),
                        use_container_width=True
                    )
                    boxplot_help()
                    st.divider()

            else:
                # Phân tích SPC cụ thể
                df_spc = df[df["SPC"] == selected_spc] # Lọc dữ liệu theo SPC đã chọn
                product = select_product(df_spc) # Chọn sản phẩm cụ thể
                row = df_spc[df_spc["SP"] == product] # Lấy dòng dữ liệu của sản phẩm đó
                current_std = std_map[selected_spc] # Lấy bản đồ tiêu chuẩn cho SPC đã chọn
                actual = row[processes].values.flatten().tolist() # Lấy giá trị thực tế của các processes
                std = std_map[selected_spc] # Lấy bản đồ tiêu chuẩn cho SPC đã chọn

                actual_pct = [(actual[i] / std[p] * 100) if std[p] > 0 else 100
                            for i, p in enumerate(processes)] # Tính phần trăm thực tế so với tiêu chuẩn
                
                st.markdown(f'<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">番号機械: {product} ({selected_spc})</h2>', unsafe_allow_html=True)                

                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(radar(processes, actual_pct), use_container_width=True)
                with c2:
                    st.plotly_chart(
                        compare_bar(processes, actual, [std[p] for p in processes]),
                        use_container_width=True
                    )

                # Hiển thị bảng so sánh chi tiết
                with st.expander(f"📊 詳しい分析コード {product}", expanded=True):
                    total_act = row['totalTime'].iloc[0]
                    total_std = sum(current_std.values())
                    st.write(f"**実際の総時間:** {total_act:.1f}分 (標準: {total_std}分)")

                    comp_data = []
                    for p in processes:
                        act = row[p].iloc[0]
                        std_val = current_std[p]
                        comp_data.append({
                            "工程": p,
                            "実際（分）": f"{act:.1f}",
                            "標準（分）": f"{std_val}",
                            "効率": f"{(std_val / act * 100):.1f}%"
                        })

                    st.table(pd.DataFrame(comp_data))

                # Phân tích SPC tổng thể
                st.markdown(f'<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">{selected_spc}の概要</h2>', unsafe_allow_html=True)                
                std_total = sum(std.values()) # Tổng thời gian tiêu chuẩn cho SPC đã chọn
                avg_act = df_spc["totalTime"].mean() # Trung bình thời gian thực tế cho SPC đã chọn
                eff_val = efficiency(std_total, avg_act) # Hiệu suất cho SPC đã chọn
                eff_df = df_spc.copy()  # DataFrame sao chép để tính hiệu suất từng process
                for p in processes:
                    eff_df[p] = (std[p] / eff_df[p] * 100).round(1) # Tính hiệu suất từng process
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(
                        process_bar(df_spc, processes, std_total, f"進程の分布 - {selected_spc} "),
                        use_container_width=True
                    )
                    with st.expander("📌 時間のパラメータ", expanded=True):
                        st.write(f"**標準時間（分）:** {std_total}")
                        st.write(f"**実際の平均（分）:** {avg_act:.1f}")
                        color = "green" if eff_val >= 100 else "red"
                        st.markdown(f"**効率:** :{color}[{eff_val:.1f}%]")

                with col2:
                    st.plotly_chart(
                            efficiency_heatmap(eff_df, processes, f"ヒートマップ効率 (%) - {selected_spc}"),
                            use_container_width=True
                    )
                    with st.expander("📊 効率と弱点の説明", expanded=True):
                        # Tìm tiến trình chậm nhất (Bottleneck)
                        
                        avg_eff_per_proc = eff_df[processes].mean()
                        bottleneck_proc = avg_eff_per_proc.idxmin()
                        bottleneck_val = avg_eff_per_proc.min()

                        # Tính hiệu suất tổng dựa trên các biến đã định nghĩa trước đó
                        # Lưu ý: Đảm bảo std_total và avg_actual_total đã được tính ở đoạn code phía trên
                        eff_total = (std_total / avg_act) * 100
                        
                        # Tìm sản phẩm yếu nhất - Cần dùng đúng set_index('SP')
                            
                        st.write(f"**平均効率:** {eff_total:.1f}%")
                        st.write(f"**ボトルネック:** {bottleneck_proc} ({bottleneck_val:.1f}%)")
                        
                        # worst_prod lúc này sẽ là String (ví dụ: '01191744') nhờ bước ép kiểu lúc read_excel
                        st.markdown(f"**注意製品:** :red[{worst_product(eff_df, processes)}]")

                st.plotly_chart(
                    process_boxplot(df_spc, processes, selected_spc),
                    use_container_width=True
                )
                boxplot_help()
                st.divider()
                # Hiển thị dữ liệu gốc
                st.markdown(f'<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">元データ</h2>', unsafe_allow_html=True)                
                # Lúc này df_filtered luôn tồn tại (là df_full nếu chọn 'Tất cả', hoặc df đã lọc)
                st.dataframe(df_spc, use_container_width=True)
                    
        except Exception as e:
            st.sidebar.error(f"❌ データの読み込み中にエラーが発生しました: {e}")
            st.stop()