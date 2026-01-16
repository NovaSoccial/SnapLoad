import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="SnapLoad Pro", page_icon="🚀")

# Modern Arayüz
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: #6c5ce7; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SnapLoad Pro")

url = st.text_input("Video Linkini Yapıştır lo:", placeholder="https://www.instagram.com/reels/...")

if st.button("HAYDİ İNDİR"):
    if not url:
        st.error("Link boş kanka!")
    else:
        with st.spinner('Instagram'ın duvarlarını zorluyorum...'):
            try:
                ydl_opts = {
                    'quiet': False, # Hata ayıklama için açık kalsın
                    'no_warnings': False,
                    # Instagram'ı kandıran özel kimlik bilgileri:
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
                        'Accept': '*/*',
                        'X-IG-App-ID': '936619743392459', # Instagram Android App ID
                        'X-ASBD-ID': '129477',
                        'X-IG-WWW-Claim': '0',
                    },
                    'format': 'best',
                    'outtmpl': 'snapload_file.%(ext)s',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                with open(filename, "rb") as f:
                    st.success("İnat ettim ve indirdim!")
                    st.download_button("💾 TELEFONA KAYDET", f, file_name=filename)
                
                os.remove(filename)

            except Exception as e:
                st.error(f"Yine engel yedik lo! Hata şu: {str(e)[:100]}...")
                st.info("Kanka Instagram bu ara çok fena. YouTube veya TikTok linki denesene bir, onlar çalışıyor mu?")

st.markdown("---")
st.caption("Şafak Vakti ve WordZen kalitesiyle... 😎")
