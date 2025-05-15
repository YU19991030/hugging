import streamlit as st
import requests
import base64

# ✅ 替換為你的後端 API 網址（ngrok 或 Render）
API_BASE = " https://0f58-125-228-143-171.ngrok-free.app"

st.set_page_config(page_title="📇 名片辨識系統", layout="centered")
st.title("📷 拍照名片辨識")

st.header("📸 拍照辨識名片")
img_file = st.camera_input("請拍攝名片")

if img_file:
    st.image(img_file, caption="名片預覽", use_column_width=True)

    img_bytes = img_file.getvalue()
    base64_img = base64.b64encode(img_bytes).decode("utf-8")
    payload = {"image": f"data:image/jpeg;base64,{base64_img}"}

    with st.spinner("🔍 OCR 辨識中..."):
        try:
            res = requests.post(f"{API_BASE}/ocr", json=payload)
            text = res.json().get("text", "")
            st.text_area("📄 名片辨識結果", value=text, height=200)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")

st.write("🚀 App 啟動成功！")
