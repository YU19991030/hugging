import streamlit as st
import requests
import base64

# ✅ Render 上的 FastAPI 後端網址
API_BASE = "https://streamlit-ocr-whisper.onrender.com"

st.set_page_config(page_title="📇 名片辨識系統", layout="centered")
st.title("📇 名片辨識 + 語音備註系統")

# ---------------------
# 📸 名片辨識功能區塊
# ---------------------
st.header("📷 拍照辨識名片")
img_file = st.camera_input("請拍攝名片")

if img_file:
    st.image(img_file, caption="名片預覽", use_column_width=True)

    with st.spinner("🔍 OCR 辨識中..."):
        try:
            files = {"file": img_file}
            res = requests.post(f"{API_BASE}/ocr", files=files)
            text = res.json().get("text", "")
            st.text_area("📄 名片辨識結果", value=text, height=200)
        except Exception as e:
            st.error(f"❌ OCR 發生錯誤：{e}")

# ---------------------
# 🎤 語音備註功能區塊
# ---------------------
st.header("🎤 上傳語音備註")
audio_file = st.file_uploader("請上傳語音檔案（支援 wav / mp3 / m4a）", type=["wav", "mp3", "m4a"])

if audio_file:
    st.audio(audio_file, format=audio_file.type)

    with st.spinner("🔊 Whisper 語音辨識中..."):
        try:
            files = {"file": audio_file}
            res = requests.post(f"{API_BASE}/whisper", files=files)
            transcript = res.json().get("text", "")
            st.text_area("📝 語音辨識結果", value=transcript, height=150)
        except Exception as e:
            st.error(f"❌ Whisper 發生錯誤：{e}")

# ---------------------
# ✅ 狀態提示
# ---------------------
st.write("🚀 App 啟動成功！")
