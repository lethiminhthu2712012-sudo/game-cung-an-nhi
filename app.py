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

# --- CSS TÙY CHỈNH GIAO DIỆN HỒNG & DÒNG DONATE CỐ ĐỊNH GÓC TRÁI ---
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

    /* DÒNG THÔNG TIN DONATE GÓC DƯỚI BÊN TRÁI MÀN HÌNH */
    .donate-footer {
        position: fixed;
        bottom: 12px;
        left: 15px;
        background: rgba(0, 0, 0, 0.4);
        color: #ffffff;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: bold;
        backdrop-filter: blur(4px);
        z-index: 9999;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
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
    st.markdown("<h4 style='text-align: center; color: white; margin-bottom: 5px;'>🐶 BẠN</h4>", unsafe_allow_html=True)
    if os.path.exists("assets/dog.jpg"):
        st.image("assets/dog.jpg", use_container_width=True)
    else:
        st.error("Không tìm thấy assets/dog.jpg")
        
    st.markdown(f"""
    <div class='hp-bar-container'>
        <div class='hp-bar-fill' style='width: {st.session_state.player_hp}%;'></div>
    </div>
    <p style='text-align:center; color:white; font-weight:bold; margin-top:3px;'>HP: {st.session_state.player_hp}/100</p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<h4 style='text-align: center; color: white; margin-bottom: 5px;'>👶 AN NHI</h4>", unsafe_allow_html=True)
    if os.path.exists("assets/annhi.jpg"):
        st.image("assets/annhi.jpg", use_container_width=True)
    else:
        st.error("Không tìm thấy assets/annhi.jpg")
        
    st.markdown(f"""
    <div class='hp-bar-container'>
        <div class='hp-bar-fill' style='width: {st.session_state.bot_hp}%;'></div>
    </div>
    <p style='text-align:center; color:white; font-weight:bold; margin-top:3px;'>HP: {st.session_state.bot_hp}/100</p>
    """, unsafe_allow_html=True)

st.divider()

placeholder = st.empty()

# --- KHỞI TẠO BẢNG DỊCH NƯỚC ĐI ĐỂ TÍNH TỶ LỆ 10% ---
winning_move_against = {
    "✌️ Kéo": "✊ Búa",
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
    st.write("### 🎯 Chọn nước đi của bạn:")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    user_choice = None
    if btn_col1.button("✌️ Kéo", use_container_width=True):
        user_choice = "✌️ Kéo"
    if btn_col2.button("✊ Búa", use_container_width=True):
        user_choice = "✊ Búa"
    if btn_col3.button("🖐️ Bao", use_container_width=True):
        user_choice = "🖐️ Bao"

    if user_choice:
        # 1. Đếm ngược 3 2 1
        for i in range(3, 0, -1):
            placeholder.markdown(f"<div class='countdown-text'>{i}</div>", unsafe_allow_html=True)
            time.sleep(0.5)
        
        # 2. LOGIC TỶ LỆ THẮNG 10%:
        chance = random.randint(1, 100)
        if chance <= 10:
            bot_choice = losing_move_against[user_choice]  # Người chơi thắng (10%)
        else:
            bot_choice = winning_move_against[user_choice] # Người chơi thua (90%)
        
        # 3. Hiển thị NƯỚC ĐI TO KHỔNG LỒ
        moves_html = f"""
        <div class='show-moves-box'>
            <div style='display: flex; justify-content: space-around; align-items: center;'>
                <div class='move-item'>🐶 Bạn<br><span style='font-size: 65px;'>{user_choice}</span></div>
                <div style='font-size: 40px; font-weight: 900; color: #ffeb3b;'>VS</div>
                <div class='move-item'>👶 An Nhi<br><span style='font-size: 65px;'>{bot_choice}</span></div>
            </div>
        </div>
        """
        placeholder.markdown(moves_html, unsafe_allow_html=True)
        time.sleep(1.2)

        # 4. Hiển thị KẾT QUẢ
        if user_choice == bot_choice:
            placeholder.markdown("<div class='big-result-draw'>🤝 HÒA RỒI!</div>", unsafe_allow_html=True)
            time.sleep(1.2)
        elif (user_choice == "✌️ Kéo" and bot_choice == "🖐️ Bao") or \
             (user_choice == "✊ Búa" and bot_choice == "✌️ Kéo") or \
             (user_choice == "🖐️ Bao" and bot_choice == "✊ Búa"):
            placeholder.markdown("<div class='big-result-win'>🎉 BẠN THẮNG!</div>", unsafe_allow_html=True)
            st.session_state.bot_hp = max(0, st.session_state.bot_hp - 20)
            st.session_state.effect_audio = "win_sound.mp3"
            time.sleep(1.2)
        else:
            placeholder.markdown("<div class='big-result-lose'>💔 BẠN THUA!</div>", unsafe_allow_html=True)
            st.session_state.player_hp = max(0, st.session_state.player_hp - 20)
            st.session_state.effect_audio = "lose_sound.mp3"
            time.sleep(1.2)
            
        placeholder.empty()
        st.rerun()
