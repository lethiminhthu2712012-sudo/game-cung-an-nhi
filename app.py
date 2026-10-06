import streamlit as st
import random
import time
import base64
import os

# Cấu hình trang vừa gọn trong màn hình máy tính
st.set_page_config(
    page_title="Oẳn Tù Tì Cùng An Nhi",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH GIAO DIỆN HÌNH NỀN & NÚT BẤM TO KHỔNG LỒ ---
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
    
    /* ĐỔI HÌNH NỀN MỚI BẤT KỲ */
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
    
    /* ĐẾM NGƯỢC GIỮA MÀN HÌNH, SIÊU TO VÀ NỔI BẬT */
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
        animation: zoomIn 0.3s ease;
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

    /* CHỮ THẮNG / THUA TO GIỮA MÀN HÌNH */
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

    /* PHÓNG TO 3 NÚT CHỌN NƯỚC ĐI */
    div.stButton > button {
        height: 70px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg, #ff75ac 0%, #ff4757 100%) !important;
        color: white !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, #ff4757 0%, #ff75ac 100%) !important;
    }

    /* DÒNG THÔNG TIN DONATE GÓC DƯỚI BÊN TRÁI MÀN HÌNH */
    .donate-footer {
        position: fixed;
        bottom: 12px;
        left: 15px;
        background: rgba(0, 0, 0, 0.6);
        color: #ffffff;
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: bold;
        backdrop-filter: blur(5px);
        z-index: 9999;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Hiển thị dòng Donate cố định ở góc trái
st.markdown("<div class='donate-footer'>💌 Muốn donate liên hệ : Minh Thư (Facebook)</div>", unsafe_allow_html=True)

# --- KHỞI TẠO TRẠNG THÁI GAME ---
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 100
if 'bot_hp' not in st.session_state:
    st.session_state.bot_hp = 100
if 'effect_audio' not in st.session_state:
    st.session_state.effect_audio = None

# --- HÀM PHÁT ÂM THANH HIỆU ỨNG THẮNG/THUA ---
def play_sound_effect(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            sound_html = f"""
                <iframe src="data:audio/mp3;base64,{b64}" allow="autoplay" id="audio" style="display:none"></iframe>
                <audio autoplay style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(sound_html, unsafe_allow_html=True)

# --- TIÊU ĐỀ GAME ---
st.markdown("<div class='title-text'>💖 OẮN TÙ TÌ CÙNG AN NHI 💖</div>", unsafe_allow_html=True)

# Bật/Tắt Nhạc Nền
with st.expander("🎵 Bật/Tắt Nhạc Nền TikTok"):
    if os.path.exists("assets/bg_sound.mp3"):
        st.audio("assets/bg_sound.mp3", loop=True)

# Phát âm thanh hiệu ứng nếu có
if st.session_state.effect_audio:
    play_sound_effect(f"assets/{st.session_state.effect_audio}")
    st.session_state.effect_audio = None

# --- KHUNG HIỂN THỊ 2 NHÂN VẬT & MÁU ---
col1, col2, col3 = st.columns([4, 1.5, 4])

with col1:
    st.markdown("<h4 style='text-align: center;
