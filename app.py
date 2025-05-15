import streamlit as st
import requests

API_BASE = "https://streamlit-ocr-whisper.onrender.com"

st.set_page_config(page_title="📇 名片辨識系統", layout="centered")
st.title("📇 名片辨識 + 語音備註系統")

# ------------------------
# 📷 名片 OCR 拍照上傳
# ------------------------
st.header("📷 拍照辨識名片")
img_file = st.camera_input("請拍攝名片")

if img_file:
    st.image(img_file, caption="名片預覽", use_container_width=True)
    with st.spinner("🔍 OCR 辨識中..."):
        try:
            files = {"file": ("image.jpg", img_file.getvalue(), "image/jpeg")}
            res = requests.post(f"{API_BASE}/ocr", files=files)
            res.raise_for_status()
            text = res.json().get("text", "")
            st.text_area("📄 名片辨識結果", value=text, height=200)
        except Exception as e:
            st.error(f"❌ OCR 發生錯誤：{e}")

# ------------------------
# 🎤 上傳語音備註
# ------------------------
st.header("🎤 上傳語音備註")
audio_file = st.file_uploader("請上傳語音檔案（支援 wav / mp3 / m4a）", type=["wav", "mp3", "m4a"])

if audio_file:
    st.audio(audio_file, format="audio/wav")
    with st.spinner("🔊 Whisper 語音辨識中..."):
        try:
            files = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}
            res = requests.post(f"{API_BASE}/whisper", files=files)
            res.raise_for_status()
            transcript = res.json().get("text", "")
            st.text_area("📝 語音辨識結果", value=transcript, height=150)
        except Exception as e:
            st.error(f"❌ Whisper 發生錯誤：{e}")

st.write("🚀 App 啟動成功！")
