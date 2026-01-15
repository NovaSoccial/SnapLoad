import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="SnapLoad Pro - Video & MP3 Downloader", page_icon="📥")

st.title("🚀 SnapLoad Pro")
st.write("YouTube, Instagram, TikTok, X üzerinden Video veya MP3 indir!")

# Kullanıcı Girişleri
url = st.text_input("Linkini buraya yapıştır:", placeholder="https://...")
format_type = st.radio("Format Seçin:", ["Video (MP4)", "Ses (MP3)"])

# Kalite Seçenekleri (Sadece Video için)
quality = "best"
if format_type == "Video (MP4)":
    quality = st.selectbox("Kalite Seçin:", ["En Yüksek", "1440p (2K)", "1080p", "720p", "480p", "360p", "En Düşük"])

if st.button("Hazırla ve İndir"):
    if not url:
        st.warning("Lütfen bir link gir!")
    else:
        with st.spinner('SnapLoad işlem yapıyor...'):
            try:
                # Kalite Mapping (Haritalama)
                quality_map = {
                    "En Yüksek": "bestvideo+bestaudio/best",
                    "1440p (2K)": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
                    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                    "En Düşük": "worstvideo+worstaudio/worst"
                }

                # yt-dlp Ayarları
                if format_type == "Ses (MP3)":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'snapload_audio.%(ext)s',
                    }
                    ext = "mp3"
                else:
                    ydl_opts = {
                        'format': quality_map.get(quality, "best"),
                        'outtmpl': 'snapload_video.%(ext)s',
                        'merge_output_format': 'mp4',
                    }
                    ext = "mp4"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    # MP3 dönüşümünde dosya adı değişebilir, o yüzden kontrol edelim
                    if format_type == "Ses (MP3)":
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                with open(filename, "rb") as file:
                    st.success("Hazır! Aşağıdaki butona tıkla.")
                    st.download_button(
                        label=f"📥 {format_type} Dosyasını İndir",
                        data=file,
                        file_name=f"SnapLoad_{ext}." + ext,
                        mime=f"{"audio" if ext=='mp3' else "video"}/{ext}"
                    )
                
                os.remove(filename) # Sunucuda yer kaplamasın

            except Exception as e:
                st.error(f"Hata: {e}")

st.markdown("---")
st.caption("SnapLoad - Tüm platformları destekler.")
