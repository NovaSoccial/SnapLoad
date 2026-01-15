import streamlit as st
import yt_dlp
import os

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="SnapLoad Pro", page_icon="🚀", layout="centered")

# --- ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Arka plan ve yazı tipi */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d3436 100%);
        color: white;
    }
    /* Giriş kutusu */
    .stTextInput input {
        border-radius: 15px !important;
        border: 2px solid #6c5ce7 !important;
        background-color: #2d3436 !important;
        color: white !important;
        padding: 15px !important;
    }
    /* Ana Buton */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background: linear-gradient(45deg, #6c5ce7, #a29bfe);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.6);
    }
    /* Başlık stili */
    h1 {
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Trebuchet MS', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ARAYÜZ ---
st.write(f"<h1 style='text-align: center;'>🚀 SnapLoad Pro</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center; opacity: 0.8;'>Instagram, YouTube, TikTok ve X Videolarını Kap ve İndir!</p>", unsafe_allow_html=True)

# Link Girişi
url = st.text_input("", placeholder="Video linkini buraya yapıştırın...")

# Seçenekler
col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Dosya Türü", ["Video (MP4)", "Ses (MP3)"])
with col2:
    quality = st.selectbox("Kalite", ["1080p", "720p", "480p", "360p", "En Yüksek", "En Düşük"])

st.markdown("<br>", unsafe_allow_html=True)

# --- İNDİRME MOTORU ---
if st.button("ŞİMDİ İNDİR"):
    if not url:
        st.warning("Kanka önce bir link yapıştırman lazım!")
    else:
        with st.spinner('SnapLoad videoyu işliyor, lütfen bekle...'):
            try:
                # Kalite Ayarları
                quality_map = {
                    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                    "En Yüksek": "bestvideo+bestaudio/best",
                    "En Düşük": "worstvideo+worstaudio/worst"
                }

                # Ortak Ayarlar (Instagram Engelini Aşmak İçin Headers eklendi)
                common_opts = {
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Referer': 'https://www.google.com/',
                    },
                    'nocheckcertificate': True,
                    'quiet': True,
                    'no_warnings': True,
                }

                if format_type == "Ses (MP3)":
                    ydl_opts = {
                        **common_opts,
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'snapload_audio.%(ext)s',
                    }
                else:
                    ydl_opts = {
                        **common_opts,
                        'format': quality_map.get(quality, "best"),
                        'outtmpl': 'snapload_video.mp4',
                        'merge_output_format': 'mp4',
                    }

                # İndirme İşlemi
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if format_type == "Ses (MP3)":
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                # Başarı Mesajı ve Dosya Gönderme
                with open(filename, "rb") as f:
                    st.success("İşlem Başarılı! Dosyan hazır.")
                    st.download_button(
                        label="💾 DOSYAYI KAYDET",
                        data=f,
                        file_name=f"SnapLoad_{filename}",
                        mime="video/mp4" if format_type == "Video (MP4)" else "audio/mpeg"
                    )
                
                os.remove(filename) # Temizlik

            except Exception as e:
                st.error(f"Bir hata oluştu: Link gizli olabilir veya sunucu meşgul olabilir.")
                st.info("İpucu: Birkaç dakika sonra tekrar denemek genellikle sorunu çözer.")

# Footer
st.markdown("<p style='text-align: center; margin-top: 50px; font-size: 0.8em;'>SnapLoad © 2026 | Reklamsız ve Hızlı</p>", unsafe_allow_html=True)
