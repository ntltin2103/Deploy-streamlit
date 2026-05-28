"""
Dự án 1: Quản lý đơn hàng
Fiel: don_hang.csv
Layout: Sử dụng Tabs (5 tabs)
Yêu cầu:
Tính tự động cột thanh_tien = so_luong * dongia
Metrics: Tổng đơn, theo trạng thái, doanh thu từ đơn "Đã giao"
Tạo sidebar:
    - sidebar Danh sách: Lọc theo Trạng thái, Sản phẩm, Khách hàng + Download CSV
    - sidebar Thêm: Cho phép nhập khách hàng mới ("Khác"), tự dsinh mã DH001, có phần Xem trước
    - sidebar Sửa 7 Xóa: Chọn theo ma_don
    - sidebar Thống kê: 3 biểu đồ (barh, pie, bar) + chức năng Upload file để ghi đè dữ liệu    
"""
import streamlit as st
import matplotlib.pyplot as plt
from helper import data_source,load_data
import pandas as pd
import datetime as dt
import time

st.set_page_config(page_title = 'Web bán hàng', layout='wide')
st.title('QUẢN LÝ BÁN HÀNG', text_alignment = 'center')

# path_csv = r'E:\Cyber_soft\BTVN\Buoi_12\Project_Retail_Manage\don_hang.csv'
# path_csv_test = r'E:\Cyber_soft\BTVN\Buoi_12\Project_Retail_Manage\don_hang_test.csv'
path_csv = 'don_hang.csv'
path_csv_test = 'don_hang_test.csv'
df = data_source(path_csv)
df_test = data_source(path_csv_test)

menu = st.sidebar.selectbox('Menu',['Trang chủ','Danh sách','Thêm hàng','Sửa & Xóa','Thống kê'])
if menu == 'Trang chủ':
    st.header('Metric tổng quan')
    so_don = len(df)
    st.metric('Tổng đơn',so_don, border = True)
    col_1,col_2,col_3,col_4 = st.columns(4)
    with col_1:
        don_huy = len(df[df['trang_thai'] == 'Huy'])
        st.metric('Số đơn hủy', don_huy, border = True )
    with col_2:
        don_da_giao = len(df[df['trang_thai'] == 'Da giao'])
        st.metric('Số đơn đã giao', don_da_giao, border = True )
    with col_3:
        don_dang_giao = len(df[df['trang_thai'] == 'Dang giao'])
        st.metric('Số đơn đã giao', don_dang_giao, border = True )
    with col_4:
        don_cho = len(df[df['trang_thai'] == 'Cho xu ly'])
        st.metric('Số đơn đã giao', don_cho, border = True )
    doanh_thu_da_giao = df[df['trang_thai'] == 'Da giao']['thanh_tien'].sum()
    st.metric(label="Tổng Doanh Thu Đã Giao", value = f'{doanh_thu_da_giao:,.0f} VND',border = True )
elif menu == 'Danh sách':
    st.header('Xem danh sách hàng hóa theo trạng thái')
    st.subheader('Danh sách tổng')
    st.dataframe(df)
    st.write('---')
    df_current = df.copy()
    #lọc danh sách
    list_options_ds = df_current['trang_thai'].unique()
    loc_ds = st.selectbox(
        'Danh sách trạng thái', 
        options = list_options_ds,
        index = None,
        placeholder="Chọn một trạng thái..."
    )
    if loc_ds:
        # Thay vì ghi 'Huy', ta truyền biến loc_ds vào
        df_current = df_current[df_current['trang_thai'] == loc_ds] 
        
        st.write(f"### Danh sách đơn hàng: {loc_ds}")
        # st.dataframe(df_current)
    #lọc sản phẩm
    list_options_sp = df_current['san_pham'].unique()
    loc_sp = st.selectbox(
        'Danh sách sản phẩm',
        options = list_options_sp,
        index = None,
        placeholder = "Chọn sản phẩm ..."
    )
    if loc_sp:
        df_current = df_current[df_current['san_pham'] == loc_sp] 
        
        st.write(f"### Danh sách đơn hàng: {loc_sp}")
        # st.dataframe(df_current)
    
    #Lọc DS KH
    list_options_kh = df_current['khach_hang'].unique()
    loc_kh = st.selectbox(
        'Danh sách Khách hàng',
        options = list_options_kh,
        index = None,
        placeholder = "Chọn Khách hàng ..."
    )
    if loc_kh:
        df_current = df_current[df_current['khach_hang'] == loc_kh] 
        st.write(f"### Tên khách hàng: {loc_kh}")
        st.dataframe(df_current)
    df_download = df[(df['trang_thai'] == loc_ds)
                & (df['san_pham']== loc_sp)
                & (df['khach_hang']== loc_kh)
                    ]
    st.download_button('Tải file',
                       data = df_download.to_csv(index = False),
                       file_name = 'Danh_sach_KH.csv',
                       mime='text/csv'
                       )
##Menu "Thêm hàng"
elif menu == 'Thêm hàng':
    st.header('Thêm hàng mới')
    with st.form('Form nhập hàng'):
        don_hang = f"DH{len(df) + 1:03d}"
        khach_hang = st.text_input('Nhập tên KH')
        san_pham = st.selectbox('Chọn sản phẩm', list(df['san_pham'].unique()))
        so_luong = st.number_input('Điền số lượng', min_value = 1, max_value = 100, step = 1)
        don_gia = df[df['san_pham'] == san_pham]['don_gia'].mode()[0]
        trang_thai = st.selectbox('Danh sách trạng thái',list(df["trang_thai"].unique()))
        ngay_dat = st.date_input(
                    'Chọn ngày',
                    min_value=dt.datetime(2026, 1, 1),
                    max_value=dt.datetime.today()
                    )
        thanh_tien = so_luong * don_gia
        submit = st.form_submit_button("Submit")
        if submit:
            ds_hang_moi = {
                "ma_don" : don_hang,
                "khach_hang" : khach_hang,
                "san_pham" : san_pham,
                "so_luong" : so_luong,
            	"don_gia": don_gia,
            	"trang_thai" : trang_thai,
                "ngay_dat" : ngay_dat,
            	"thanh_tien" : thanh_tien
            }
            dong_moi = pd.DataFrame([ds_hang_moi])
            df_moi = pd.concat([df,dong_moi], ignore_index = True)
            df_moi.to_csv(path_csv, index = False)
            st.success('Thêm hàng thành công')
            time.sleep(1.5)
            st.rerun()
# Menu "Sửa & Xóa"
elif menu == 'Sửa & Xóa':
    st.header('Xóa hàng')
    with st.form('Form nhập hàng'):
        ma_don = st.selectbox('Chọn mã hàng',list(df['ma_don'].unique()))
        new_df = df[df['ma_don'] != ma_don ]
        submit = st.form_submit_button('Xóa hàng')
        if submit:
            new_df.to_csv(path_csv, index = False)
            st.success('Thêm hàng thành công')
            time.sleep(1.5)
            st.rerun()
# Menu "Thông kê"
elif menu == 'Thống kê':
    with st.container(border=True):
        st.subheader('Top 5 sản phẩm có doanh thu cao nhất')
        df_top_5 = df.groupby('san_pham')['thanh_tien'].sum().reset_index().sort_values(by='thanh_tien').head()
        fig, ax = plt.subplots(figsize = (6,4))
        ax.barh(df_top_5['san_pham'],df_top_5['thanh_tien'])
        st.pyplot(fig)
    with st.container(border=True):
        st.subheader('Tỷ lệ đơn hàng')
        df_ty_le_trang_thai = df.groupby('trang_thai')['ma_don'].count().reset_index()
        fig, ax = plt.subplots(figsize = (6,4))
        ax.pie(df_ty_le_trang_thai['ma_don'], labels = df_ty_le_trang_thai['trang_thai'], autopct = '%1.1f%%')
        st.pyplot(fig)
    new_df_2 = st.file_uploader('Upload file csv', type = 'csv')

# tự dsinh mã DH001, có phần Xem trước
# elif menu == 'Thêm hàng':
# #     tab_list, tab_add, tab_edit, tab_stats = st.tabs([
# #     "🔍 Danh Sách", "➕ Thêm Đơn Hàng", "✏️ Sửa & Xóa", "📈 Thống Kê"
# # ])

# # # --- 2. XỬ LÝ CHÍNH TRONG TAB THÊM ---
# #     with tab_add:
#         st.markdown("## Thêm Đơn Hàng Mới")
#         st.markdown("---")
        
#         # THUẬT TOÁN: TỰ ĐỘNG SINH MÃ ĐƠN HÀNG TIẾP THEO (Ví dụ: DH100 -> DH101)
#         if not df.empty and 'ma_don' in df.columns:
#             # Cắt chuỗi bỏ 'DH' ở đầu, chuyển sang số, tìm max và cộng 1
#             try:
#                 max_id = df['ma_don'].apply(lambda x: int(str(x)[2:])).max()
#                 next_id = f"DH{max_id + 1:03d}"
#             except:
#                 next_id = f"DH{len(df) + 1:03d}"
#         else:
#             next_id = "DH001"

#         # KHỐI 1: THÔNG TIN HỆ THỐNG TỰ ĐỘNG (LAYOUT 2 CỘT)
#         col1, col2 = st.columns(2)
#         with col1:
#             st.text_input("🔑 Mã đơn hàng (Hệ thống tự sinh)", value=next_id, disabled=True)
#         with col2:
#             today = datetime.date.today()
#             st.date_input("📅 Ngày đặt hàng (Mặc định)", value=today, disabled=True)

#         st.markdown("### 📋 Thông tin khách hàng & Sản phẩm")
#         col3, col4 = st.columns(2)
        
#         with col3:
#             # Lấy danh sách khách hàng duy nhất từ file của em và chèn thêm tùy chọn "Khác"
#             list_khach_hang = sorted(df['khach_hang'].dropna().unique().tolist())
#             options_khach_hang = list_khach_hang + ["Khác (Nhập mới)..."]
            
#             selected_khach = st.selectbox("👤 Chọn khách hàng", options=options_khach_hang)
            
#             # DYNAMIC UX: Nếu chọn "Khác", hiện ô text_input để nhập mới
#             if selected_khach == "Khác (Nhập mới)...":
#                 ten_khach_hang_cuoi = st.text_input("✨ Nhập tên khách hàng mới:", placeholder="Ví dụ: Nguyễn Văn A...")
#             else:
#                 ten_khach_hang_cuoi = selected_khach

#         with col4:
#             # Lấy danh sách sản phẩm thực tế từ file của em
#             list_san_pham = sorted(df['san_pham'].dropna().unique().tolist())
#             selected_sp = st.selectbox("📦 Chọn sản phẩm", options=list_san_pham)

#         st.markdown("### 💰 Chi tiết số lượng & Giá")
#         col5, col6, col7 = st.columns(3)
        
#         with col5:
#             so_luong_input = st.number_input("Số lượng", min_value=1, value=1, step=1)
#         with col6:
#             # Tìm đơn giá mặc định của sản phẩm đó trong lịch sử để gợi ý cho user nhập liệu nhanh hơn
#             gia_mac_dinh = int(df[df['san_pham'] == selected_sp]['don_gia'].iloc[0]) if selected_sp in df['san_pham'].values else 0
#             don_gia_input = st.number_input("Đơn giá (VNĐ)", min_value=0, value=gia_mac_dinh, step=10000)
#         with col7:
#             # REAL-TIME FEEDBACK: Tính toán tự động hiển thị trực quan mặt UX/UI
#             thanh_tien_tu_dong = so_luong_input * don_gia_input
#             st.metric(label="💵 Thành tiền tự động", value=f"{thanh_tien_tu_dong:,.0f} đ")

#         # Chọn trạng thái chuẩn theo dữ liệu của em
#         list_trang_thai = ['Cho xu ly', 'Dang giao', 'Da giao', 'Huy']
#         selected_status = st.selectbox("🚦 Trạng thái đơn hàng", options=list_trang_thai)

#         st.markdown("---")
#         st.markdown("### 👀 Xem trước dòng dữ liệu (Live Preview)")
        
#         # Tạo cấu trúc dòng mới khớp 100% với file CSV để người dùng đối chiếu
#         new_row_preview = {
#             "ma_don": next_id,
#             "khach_hang": ten_khach_hang_cuoi,
#             "san_pham": selected_sp,
#             "so_luong": so_luong_input,
#             "don_gia": don_gia_input,
#             "trang_thai": selected_status,
#             "ngay_dat": today
#         }
        
#         # Hiển thị bảng dữ liệu tĩnh trực quan
#         st.table([new_row_preview])

#         # NÚT XÁC NHẬN GHI VÀO DATABASE (FILE CSV)
#         if st.button(" XÁC NHẬN LƯU ĐƠN HÀNG", type="primary"):
#             # Bẫy lỗi bảo vệ dữ liệu (Validation)
#             if not ten_khach_hang_cuoi.strip():
#                 st.error(" Thất bại: Vui lòng không để trống tên khách hàng!")
#             elif don_gia_input <= 0:
#                 st.error(" Thất bại: Đơn giá sản phẩm phải lớn hơn 0!")
#             else:
#                 # Tiến hành append dữ liệu mới vào file CSV
#                 new_df = pd.DataFrame([new_row_preview])
#                 df_updated = pd.concat([df, new_df], ignore_index=True)
                
#                 # Lưu đè lại file CSV hiện tại
#                 df_updated.to_csv('don_hang.csv', index=False)
                
#                 st.success(f" Thành công: Đã ghi nhận đơn hàng {next_id} của khách hàng '{ten_khach_hang_cuoi}' vào hệ thống!")
                
#                 # Đợi 1 giây rồi tự động reload lại toàn bộ giao diện bảng để cập nhật mã tiếp theo
#                 st.rerun()
