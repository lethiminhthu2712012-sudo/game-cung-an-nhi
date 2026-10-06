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

# --- CSS TÙY CHỈNH GIAO DIỆN HỒNG & VỪA KHUNG MÀN HÌNH ---
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
    
    .stApp {
        background: linear-gradient(135deg, #ff75ac 0%, #ffa6c9 100%);
    }

    .title-text {
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }

    .hp-bar-container {
        background-color: #ddd;
        border-radius: 10px;
        height: 16px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
    }
    .hp-bar-fill {
        background-color: #2ed573;
        height: 100%;
        transition: width 0.3s ease;
    }

    .vs-text {
        font-size: 32px;
        font-weight: 900;
        color: #ffeb3b;
        text-align: center;
        margin-top: 90px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .countdown-text {
        font-size: 55px;
        font-weight: 900;
        color: #ffff00;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }
    
    /* HIỂN THỊ NƯỚC ĐI KHỔNG LỒ */
    .show-moves-box {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid rgba(255, 255, 255, 0.5);
    }
    .move-item {
        font-size: 45px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }

    /* CHỮ THẮNG / THUA TO GIỮA MÀN HÌNH */
    .big-result-win {
        font-size: 60px;
        font-weight: 900;
        color: #00ff66;
        text-align: center;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        padding: 5px;
    }
    .big-result-lose {
        font-size: 60px;
        font-weight: 900;
        color: #ff3333;
        text-align: center;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        padding: 5px;
    }
    .big-result-draw {
        font-size: 60px;
        font-weight: 900;
        color: #ffea00;
        text-align: center;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        padding: 5px;
    }

    [data-testid="stImage"] img {
        border-radius: 15px;
        height: 230px;
        object-fit: cover;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

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
