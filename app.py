import subprocess
import streamlit as st
import youtube_content_with_subtitles as yt
st.title('YouTube Video Downloader')

video_url = st.text_input('Enter YouTube Video URL')

if st.button('Download Audio'):
    if video_url:
            yt.download_audio(video_url)
            
    else:
        st.warning("Please enter a valid YouTube URL.")
