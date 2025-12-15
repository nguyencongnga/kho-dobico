import streamlit as st
import pandas as pd
import os

# 1. Cấu hình trang web
st.set_page_config(page_title="Kho Hàng Dien24h", layout="centered")
FILE_DU_LIEU = 'kho_hang.csv'

# 2. Hàm xử lý dữ liệu
def tai_du_lieu():
    if not os.path.exists(FILE_DU_LIEU):
        return pd.DataFrame(columns=['Tên Sản Phẩm', 'Số Lượng', 'Đơn Giá', 'Ghi Chú'])
    return pd.read_csv(FILE_DU_LIEU)

def luu_du_lieu(df):
    df.to_csv(FILE_DU_LIEU, index=False)

# 3. Giao diện chính
st.title("📦 Quản Lý Kho Dien24h")

# Tải dữ liệu lên
df = tai_du_lieu()

# --- PHẦN NHẬP HÀNG (Cột bên trái) ---
st.sidebar.header("📝 Nhập Mới / Nhập Thêm")
with st.sidebar.form("nhap_hang"):
    ten_sp = st.text_input("Tên sản phẩm")
    so_luong = st.number_input("Số lượng", min_value=1, step=1)
    don_gia = st.number_input("Đơn giá (VNĐ)", min_value=0, step=1000)
    ghi_chu = st.text_area("Ghi chú")
    
    nut_them = st.form_submit_button("Lưu vào kho")

    if nut_them and ten_sp:
        # Kiểm tra xem hàng đã có chưa để cộng dồn
        if ten_sp in df['Tên Sản Phẩm'].values:
            df.loc[df['Tên Sản Phẩm'] == ten_sp, 'Số Lượng'] += so_luong
            st.success(f"Đã cập nhật số lượng cho '{ten_sp}'!")
        else:
            dong_moi = pd.DataFrame([{
                'Tên Sản Phẩm': ten_sp, 
                'Số Lượng': so_luong, 
                'Đơn Giá': don_gia, 
                'Ghi Chú': ghi_chu
            }])
            df = pd.concat([df, dong_moi], ignore_index=True)
            st.success(f"Đã thêm mới '{ten_sp}'!")
        
        luu_du_lieu(df)
        st.rerun()

# --- PHẦN HIỂN THỊ (Màn hình chính) ---
col1, col2 = st.columns(2)
col1.metric("Tổng mặt hàng", len(df))
col2.metric("Tổng giá trị kho", f"{(df['Số Lượng'] * df['Đơn Giá']).sum():,.0f} VNĐ")

st.dataframe(df, use_container_width=True)

# --- PHẦN XÓA HÀNG ---
st.divider()
if not df.empty:
    with st.expander("🗑️ Xóa sản phẩm"):
        sp_can_xoa = st.selectbox("Chọn sản phẩm cần xóa", df['Tên Sản Phẩm'].unique())
        if st.button("Xác nhận xóa"):
            df = df[df['Tên Sản Phẩm'] != sp_can_xoa]
            luu_du_lieu(df)
            st.success("Đã xóa xong!")
            st.rerun()