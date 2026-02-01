import pandas as pd
import streamlit as st
from config.settings import setup_page, render_title
from data.loader import load_data
from ui.sidebar import upload, select_spc, select_product
from charts.bar import process_bar
from charts.heatmap import efficiency_heatmap
from charts.boxplot import process_boxplot
from charts.radar import radar
from charts.compare import compare_bar
from ui.explainers import boxplot_help, stack_bar_help, heatmap_help

setup_page()
render_title()

uploaded = upload()

if not uploaded:
    st.info("👋 ようこそ！Excelファイルをアップロードして分析を開始してください")
    st.stop()

if uploaded is not None:
    with st.spinner("⏳ データを処理中..."):
        try:
            # Tải và chuẩn bị dữ liệu
            df, std_map, processes = load_data(uploaded) 
            # df: dữ liệu đầy đủ
            # std_map: bản đồ tiêu chuẩn
            # processes: danh sách tiến trình

            # Lựa chọn SPC từ sidebar
            selected_spc = select_spc(std_map)
            st.sidebar.success("✅ データが正常にアップロードされました！")
            
            # Phân tích và hiển thị dữ liệu
            if selected_spc == "すべて": # Chọn tất cả SPC
                st.markdown('<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">📈 全製品のSPC分析</h2>', unsafe_allow_html=True)                
                st.write("各SPCごとの詳細な分析を以下に示します。")
                
                # Hiển thị dữ liệu gốc
                with st.expander("📊 元データ"):
                    # df la tat ca du lieu khi chon 'Tat ca'
                    st.dataframe(df, use_container_width=True)
                
                for spc, std in std_map.items(): # Lặp qua từng SPC và bản đồ tiêu chuẩn tương ứng
                    df_spc = df[df["SPC"] == spc] # Lọc dữ liệu theo SPC
                    if df_spc.empty: 
                        continue
                    
                    std_total = sum(std.values()) # Tổng thời gian tiêu chuẩn cho SPC hiện tại
                    avg_act = df_spc["totalTime"].mean()  # Trung bình thời gian thực tế cho SPC hiện tại
                    eff_val = (std_total / avg_act) * 100 # Hiệu suất cho SPC hiện tại 
                    # avg_act = df_spc["totalTime"].mean() 
                    # eff_val = efficiency(std_total, avg_act)
                    st.markdown(f"""<h3 style="color: #1f4e78; border-bottom: 2px solid #1f4e78; width: fit-content; padding-bottom: 5px;">
                                    SPC: {spc}
                                </h3>""", unsafe_allow_html=True)
                    
                    # Hiển thị biểu đồ và phân tích
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            process_bar(df_spc, processes, std_total, f"進程の分布 - {spc} "), #df_spc la du lieu loc theo spc hien tai, processes la danh sach tien trinh, std_total la tong thoi gian tieu chuan
                            use_container_width=True
                        )
                        # Hiển thị thông số thời gian
                        stack_bar_help(df_spc, std) 
                        #df_spc la du lieu loc theo spc hien tai, std la ban do tieu chuan hien tai

                    eff_df = df_spc.copy() 
                    # DataFrame sao chép để tính hiệu suất từng process

                    for p in processes:
                        eff_df[p] = (std[p] / eff_df[p] * 100).round(1) 
                        # eff_df chua hieu suat tung process, 
                        # std[p] la thoi gian tieu chuan cua process p, 
                        # eff_df[p] la thoi gian thuc te cua process p

                    with col2:
                        st.plotly_chart(
                            efficiency_heatmap(eff_df, processes, f"ヒートマップ効率 (%) - {spc}"),
                            use_container_width=True
                        )
                        heatmap_help(df_spc, std, eff_df, processes)

                    st.plotly_chart(
                        process_boxplot(df_spc, processes, spc),
                        use_container_width=True
                    )
                    # boxplot_help()
                    st.divider()

            else:
                # Phân tích SP cụ thể
                df_spc = df[df["SPC"] == selected_spc] # Lọc dữ liệu theo SPC đã chọn
                sp = select_product(df_spc) # Chọn sản phẩm cụ thể
                row = df_spc[df_spc["SP"] == sp] # Lấy dòng dữ liệu của sản phẩm đó
                current_std = std_map[selected_spc] # Lấy bản đồ tiêu chuẩn cho SPC đã chọn
                actual = row[processes].values.flatten().tolist() # Lấy giá trị thực tế của các processes
                std = std_map[selected_spc] # Lấy bản đồ tiêu chuẩn cho SPC đã chọn

                actual_pct = [(actual[i] / std[p] * 100) if std[p] > 0 else 100
                            for i, p in enumerate(processes)] # Tính phần trăm thực tế so với tiêu chuẩn
                
                st.markdown(f'<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">番号機械: {sp} ({selected_spc})</h2>', unsafe_allow_html=True)                

                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(radar(processes, actual_pct), use_container_width=True)
                with c2:
                    st.plotly_chart(
                        compare_bar(processes, actual, [std[p] for p in processes]),
                        use_container_width=True
                    )

                # Hiển thị bảng so sánh chi tiết
                with st.expander(f"📊 詳しい分析コード {sp}", expanded=True):
                    total_act = row['totalTime'].iloc[0] # Tổng thời gian thực tế
                    total_std = sum(current_std.values()) # Tổng thời gian tiêu chuẩn
                    st.write(f"**実際の総時間:** {total_act:.1f}分 (標準: {total_std}分)") # Hiển thị tổng thời gian thực tế và tiêu chuẩn

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
                eff_val = std_total / avg_act * 100 # Hiệu suất cho SPC đã chọn
                
                col1, col2 = st.columns(2)
                
                #Stacked Bar
                with col1:
                    st.plotly_chart(
                        process_bar(df_spc, processes, std_total, f"進程の分布 - {selected_spc} "),
                        use_container_width=True
                    )
                    stack_bar_help(df_spc, std)

                
                #Heatmap
                eff_df = df_spc.copy()  # DataFrame sao chép để tính hiệu suất từng process
                for p in processes:
                    eff_df[p] = (std[p] / eff_df[p] * 100).round(1) # Tính hiệu suất từng process

                with col2:
                    st.plotly_chart(
                            efficiency_heatmap(eff_df, processes, f"ヒートマップ効率 (%) - {selected_spc}"),
                            use_container_width=True
                    )
                    heatmap_help(eff_df, std, eff_df, processes)
                
                #Boxplot
                st.plotly_chart(
                    process_boxplot(df_spc, processes, selected_spc),
                    use_container_width=True
                )
                # boxplot_help()
                
                st.divider()
                
                # Hiển thị dữ liệu gốc
                st.markdown(f'<h2 style="color: #1f4e78; border-left: 5px solid #1f4e78; padding-left: 10px;">元データ</h2>', unsafe_allow_html=True)                
                st.dataframe(df_spc, use_container_width=True) #df_spc la du lieu loc theo spc da chon
                    
        except Exception as e:
            st.sidebar.error(f"❌ データの読み込み中にエラーが発生しました: {e}")
            st.stop()