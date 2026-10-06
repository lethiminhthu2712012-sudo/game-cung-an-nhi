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

# --- CSS TÙY CHỈNH GIAO DIỆN HÌNH NỀN ANIME NỮ & NÚT BẤM CHỮ KHỔNG LỒ ---
custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 850px !important;
    }
    
    /* HÌNH NỀN ANIME NỮ KHỦNG/ĐẸP */
    .stApp {
        background: url('https://images.alphacoders.com/132/1327129.png') no-repeat center center fixed;
        background-size: cover;
    }

    .title-text {
        text-align: center;
        color: #ffffff;
        font-size: 34px;
        font-weight: bold;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.7);
        margin-bottom: 15px;
        background: rgba(0, 0, 0, 0.4);
        padding: 10px;
        border-radius: 20px;
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .hp-bar-container {
        background-color: rgba(0, 0, 0, 0.4);
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
        font-size: 38px;
        font-weight: 900;
        color: #fff200;
        text-align: center;
        margin-top: 85px;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.8);
    }
    
    /* ĐẾM NGƯỢC GIỮA MÀN HÌNH */
    .countdown-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 120px;
    }
    .countdown-text {
        font-size: 95px;
        font-weight: 900;
        color: #fff200;
        text-align: center;
        text-shadow: 4px 4px 12px rgba(0,0,0,0.9);
    }
    
    /* NƯỚC ĐI TO RÕ */
    .show-moves-box {
        background: rgba(0, 0, 0, 0.6);
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
        text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
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
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        border: 2px solid #fff;
    }

    /* CHỮ "CHỌN NƯỚC ĐI CỦA BẠN" TO RÕ */
    .select-title {
        text-align: center;
        color: #ffffff;
        font-size: 32px !important;
        font-weight: 900 !important;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.8);
        margin-bottom: 20px;
        background: rgba(0,0,0,0.3);
        padding: 6px;
        border-radius: 12px;
    }

    /* PHÓNG CỰC TO NÚT CẢ KHUNG LẪN CHỮ BÊN TRONG */
    div.stButton > button {
        height: 110px !important;
        border-radius: 25px !important;
        background: linear-gradient(135deg, #ff75ac 0%, #ff4757 100%) !important;
        border: 4px solid #ffffff !important;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.2s ease !important;
    }
    /* CANH CHỮ TRONG NÚT BẤM TO RÕ (BẮT TRÚNG THẺ P) */
    div.stButton > button div p, 
    div.stButton > button p, 
    div.stButton > button {
        font-size: 36px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4) !important;
    }
    div.stButton > button:hover {
        transform: scale(1.08) !important;
        background: linear-gradient(135deg, #ff4757 0%, #ff75ac 100%) !important;
    }

    /* DONATE GÓC TRÁI */
    .donate-footer {
        position: fixed;
        bottom: 12px;
        left: 15px;
        background: rgba(0, 0, 0, 0.6);
        color: #ffffff;
        padding: 8px 14px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: bold;
        backdrop-filter: blur(6px);
        z-index: 9999;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Hiển thị dòng Donate cố định ở góc trái
st.markdown("<div class='donate-footer'>💌 Muốn donate liên hệ : Minh Thư (Facebook)</div>", unsafe_allow_html=True)

# --- KHỞI TẠO TRẠNG THÁI GAME ---
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 100
if 'bot_hp' not in st.session_state:
    st.session_state.bot_hp = 100
if 'effect_audio' not in st.session_state:
    st.session_state.effect_audio = None

# --- HÀM PHÁT ÂM THANH HIỆU ỨNG ---
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
    st.markdown("<h4 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🐶 BẠN</h4>", unsafe_allow_html=True)
    if os.path.exists("assets/dog.jpg"):
        st.image("assets/dog.jpg", use_container_width=True)
    else:
        st.error("Không tìm thấy assets/dog.jpg")
        
    st.markdown(f"""
    <div class='hp-bar-container'>
        <div class='hp-bar-fill' style='width: {st.session_state.player_hp}%;'></div>
    </div>
    <p style='text-align:center; color:white; font-weight:bold; margin-top:3px; text-shadow:1px 1px 3px #000;'>HP: {st.session_state.player_hp}/100</p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<h4 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>👶 AN NHI</h4>", unsafe_allow_html=True)
    if os.path.exists("assets/annhi.jpg"):
        st.image("assets/annhi.jpg", use_container_width=True)
    else:
        st.error("Không tìm thấy assets/annhi.jpg")
        
    st.markdown(f"""
    <div class='hp-bar-container'>
        <div class='hp-bar-fill' style='width: {st.session_state.bot_hp}%;'></div>
    </div>
    <p style='text-align:center; color:white; font-weight:bold; margin-top:3px; text-shadow:1px 1px 3px #000;'>HP: {st.session_state.bot_hp}/100</p>
    """, unsafe_allow_html=True)

st.divider()

placeholder = st.empty()

# --- BẢNG DỊCH NƯỚC ĐI CỦA MÁY ---
winning_move_against = {
    "✌️️ Kéo": "✊ Búa",
    "✊ Búa": "🖐️ Bao",
    "🖐️ Bao": "✌️ Kéo"
}

losing_move_against = {
    "✌️ Kéo": "🖐️ Bao",
    "✊ Búa": "✌️ Kéo",
    "🖐️ Bao": "✊ Búa"
}

# --- XỬ LÝ NÚT CHỌN ĐÒN VÀ ĐẾM NGƯỢC ---
if st.session_state.player_hp <= 0 or st.session_state.bot_hp <= 0:
    if st.session_state.player_hp <= 0:
        placeholder.markdown("<div class='big-result-lose'>😭 BẠN THUA CUỘC!</div>", unsafe_allow_html=True)
        st.session_state.effect_audio = "lose_sound.mp3"
    else:
        st.balloons()
        placeholder.markdown("<div class='big-result-win'>🎉 BẠN THẮNG CUỘC!</div>", unsafe_allow_html=True)
        st.session_state.effect_audio = "win_sound.mp3"
    
    if st.button("🔄 Chơi lại trận mới", use_container_width=True):
        st.session_state.player_hp = 100
        st.session_state.bot_hp = 100
        st.rerun()

else:
    st.markdown("<div class='select-title'>🎯 Chọn nước đi của bạn:</div>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    user_choice = None
    if btn_col1.button("✌️ Kéo", use_container_width=True):
        user_choice = "✌️ Kéo"
    if btn_col2.button("✊ Búa", use_container_width=True):
        user_choice = "✊ Búa"
    if btn_col3.button("🖐️ Bao", use_container_width=True):
        user_choice = "🖐️ Bao"

    if user_choice:
        # 1. ĐẾM NGƯỢC 3 2 1
        for i in range(3, 0, -1):
            placeholder.markdown(f"<div class='countdown-box'><div class='countdown-text'>{i}</div></div>", unsafe_allow
