import streamlit as st
import random
import time
import base64
import os

# Cấu hình trang
st.set_page_config(
    page_title="Oẳn Tù Tì Cùng An Nhi",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH GIAO DIỆN HÌNH NỀN & NÚT BẤM ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 850px !important;
    }
    
    /* HÌNH NỀN ĐẸP */
    .stApp {
        background: url("https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1920") no-repeat center center fixed;
        background-size: cover;
    }

    .title-text {
        text-align: center;
        color: #ffffff;
        font-size: 32px;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
        margin-bottom: 15px;
        background: rgba(0, 0, 0, 0.3);
        padding: 8px;
        border-radius: 15px;
    }

    .hp-bar-container {
        background-color: rgba(255, 255, 255, 0.4);
        border-radius: 10px;
        height: 18px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
        border: 1px solid #fff;
    }
    .hp-bar-fill {
        background-color: #ff4757;
        height: 100%;
        transition: width 0.3s ease;
    }

    .vs-text {
        font-size: 36px;
        font-weight: 900;
        color: #ffeb3b;
        text-align: center;
        margin-top: 85px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
    }
    
    /* ĐẾM NGƯỢC GIỮA MÀN HÌNH, TO VÀ NỔI BẬT */
    .countdown-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 120px;
    }
    .countdown-text {
        font-size: 85px;
        font-weight: 900;
        color: #ffff00;
        text-align: center;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8);
    }
    
    /* HIỂN THỊ NƯỚC ĐI KHỔNG LỒ */
    .show-moves-box {
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid rgba(255, 255, 255, 0.6);
    }
    .move-item {
        font-size: 40px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    }

    /* KẾT QUẢ THẮNG THUA */
    .big-result-win {
        font-size: 60px;
        font-weight: 900;
        color: #00ff66;
        text-align: center;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8);
        padding: 5px;
    }
    .big-result-lose {
        font-size: 60px;
        font-weight: 900;
        color: #ff3333;
        text-align: center;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8);
        padding: 5px;
    }
    .big-result-draw {
        font-size: 60px;
        font-weight: 900;
        color: #ffea00;
        text-align: center;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8);
        padding: 5px;
    }

    [data-testid="stImage"] img {
        border-radius: 15px;
        height: 220px;
        object-fit: cover;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        border: 2px solid #fff;
    }

    /* NÚT BẤM CHỌN NƯỚC ĐI TO */
    div.stButton > button {
        height: 70px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
