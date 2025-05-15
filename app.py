import streamlit as st
import requests
import io

# ✅ 替換為你的後端 API 網址（Render）
API_BASE = "https://streamlit-ocr-whisper.onrender.com"

st.set_page_config(page_title=" 名片辨識系統", layout="centered")
st.title(" 拍照名片辨識 +  語音備註")

# ---------- 📸 拍照辨識名片 ----------
st.header("📸 拍照辨識名片")
img_file = st.camera_input("請拍攝名片")

if img_file:
    st.image(img_file, caption="名片預覽", use_column_width=True)

    with st.spinner("🔍 OCR 辨識中..."):
        try:
            files = {"file": ("image.jpg", img_file.getvalue(), "image/jpeg")}
            res = requests.post(f"{API_BASE}/ocr", files=files)
            text = res.json().get("text", "")
            st.text_area("📄 名片辨識結果", value=text, height=200)
        except Exception as e:
            st.error(f"❌ OCR 發生錯誤：{e}")

# ---------- 🎤 語音錄製備註 ----------
st.header("🎤 錄音語音備註")
audio_file = st.audio(label="請錄製語音備註（MP3/WAV）", format="audio/wav")

if audio_file:
    with st.spinner("🎧 Whisper 語音辨識中..."):
        try:
            files = {"file": ("audio.wav", audio_file.getvalue(), "audio/wav")}
            res = requests.post(f"{API_BASE}/whisper", files=files)
            transcript = res.json().get("text", "")
            st.text_area("📝 語音轉文字結果", value=transcript, height=150)
        except Exception as e:
            st.error(f"❌ Whisper 發生錯誤：{e}")

st.write("🚀 App 啟動成功！")

