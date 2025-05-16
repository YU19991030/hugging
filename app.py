import streamlit as st
import requests

API_BASE = "https://streamlit-ocr-whisper.onrender.com"

st.set_page_config(page_title="📇 名片辨識系統", layout="centered")
st.title("📇 名片辨識 + 語音備註系統")

# ------------------------
# 📤 上傳多張名片圖片
# ------------------------
st.header("📤 上傳名片圖片（支援多張）")
img_files = st.file_uploader("請上傳名片圖片（支援 jpg/png）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if img_files:
    for img_file in img_files:
        st.image(img_file, caption=f"預覽：{img_file.name}", use_container_width=True)
        with st.spinner(f"🔍 OCR 辨識中：{img_file.name}"):
            try:
                files = {"file": (img_file.name, img_file.getvalue(), img_file.type)}
                res = requests.post(f"{API_BASE}/ocr", files=files)
                res.raise_for_status()
                text = res.json().get("text", "")
                st.text_area(f"📄 {img_file.name} 辨識結果", value=text, height=150)
            except Exception as e:
                st.error(f"❌ OCR 發生錯誤：{e}")

# ------------------------
# 🎤 語音備註錄音（streamlit-audiorecorder）
# ------------------------
from streamlit_audiorecorder import audiorecorder

st.header("🎤 語音備註錄音")
audio = audiorecorder("▶️ 開始錄音", "⏹️ 停止錄音")

if len(audio) > 0:
    st.audio(audio, format="audio/wav")
    with st.spinner("🔊 Whisper 語音辨識中..."):
        try:
            files = {"file": ("audio.wav", audio.tobytes(), "audio/wav")}
            res = requests.post(f"{API_BASE}/whisper", files=files)
            res.raise_for_status()
            transcript = res.json().get("text", "")
            st.text_area("📝 語音辨識結果", value=transcript, height=150)
        except Exception as e:
            st.error(f"❌ Whisper 發生錯誤：{e}")

st.write("🚀 App 啟動成功！")
