import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="SnapLoad Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d3436 100%); color: white; }
    .stTextInput input { border-radius: 15px !important; border: 2px solid #6c5ce7 !important; background-color: #2d3436 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 25px; background: linear-gradient(45deg, #6c5ce7, #a29bfe); color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.write("<h1 style='text-align: center;'>🚀 SnapLoad Pro</h1>", unsafe_allow_html=True)

url = st.text_input("", placeholder="Instagram veya YouTube linkini yapıştır...")

col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Format", ["Video (MP4)", "Ses (MP3)"])
with col2:
    quality = st.selectbox("Kalite", ["720p", "480p", "360p", "En Yüksek"])

if st.button("ŞİMDİ İNDİR"):
    if not url:
        st.warning("Link nerede lo?")
    else:
        with st.spinner('SnapLoad motoru çalışıyor...'):
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    # Instagram engelini aşmak için kritik ayarlar:
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Origin': 'https://www.instagram.com',
                        'Referer': 'https://www.instagram.com/',
                    },
                    'format': 'best' if format_type == "Video (MP4)" else 'bestaudio/best',
                    'outtmpl': 'snapload_file.%(ext)s',
                }

                if format_type == "Ses (MP3)":
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if format_type == "Ses (MP3)":
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                with open(filename, "rb") as f:
                    st.success("Buldum! İndirebilirsin.")
                    st.download_button(
                        label="💾 DOSYAYI KAYDET",
                        data=f,
                        file_name=f"SnapLoad_{filename}",
                        mime="video/mp4" if format_type == "Video (MP4)" else "audio/mpeg"
                    )
                os.remove(filename)

            except Exception as e:
                st.error("Instagram şu an bizi engelliyor. Lütfen 1-2 dakika sonra tekrar dene.")

st.markdown("<p style='text-align: center; margin-top: 50px;'>SnapLoad © 2026</p>", unsafe_allow_html=True)
