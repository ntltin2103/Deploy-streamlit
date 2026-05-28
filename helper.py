import pandas as pd
import datetime as dt
import streamlit as st 

def data_source(file_name):
    df = pd.read_csv(file_name)
    df['ngay_dat'] = pd.to_datetime(df['ngay_dat'], format = 'mixed')
    df['thanh_tien'] = df['so_luong'] * df['don_gia']
    # df.to_excel(file_name)
    return df

def load_data():
    try:
        df = pd.read_csv('don_hang.csv')
        # Ép kiểu dữ liệu để tránh lỗi tính toán
        df['so_luong'] = df['so_luong'].astype(int)
        df['don_gia'] = df['don_gia'].astype(int)
        return df
    except FileNotFoundError:
        st.error("Không tìm thấy file don_hang.csv! Hãy đảm bảo file nằm cùng thư mục với code.")
        return pd.DataFrame(columns=['ma_don', 'khach_hang', 'san_pham', 'so_luong', 'don_gia', 'trang_thai', 'ngay_dat'])

df = load_data()