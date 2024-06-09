import subprocess
import json
import streamlit as st

def download_youtube_video(youtube_url, output_filename):
    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        st.error("yt-dlp is not installed. Install it using 'pip install yt-dlp'")
        return
    
    # Check if ffmpeg is installed
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        st.error("ffmpeg is not installed. Download and install it from https://ffmpeg.org/download.html")
        return

    # yt-dlp command to download the best quality video in mp4 format
    command = [
        'yt-dlp',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        '-o', f"{output_filename}.%(ext)s",
        youtube_url
    ]

    try:
        subprocess.run(command, check=True)
        st.success(f"Download completed: {output_filename}.mp4")
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred: {e}")

def get_youtube_title(youtube_url):
    # yt-dlp command to extract video info in JSON format
    command = [
        'yt-dlp',
        '--dump-json',
        youtube_url
    ]

    try:
        # Run the command and capture the output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        video_info = json.loads(result.stdout)
        # Extract the title from the JSON data
        title = video_info.get('title', 'Unknown Title')
        return title
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred: {e}")
        return None

st.title("YouTube Video Downloader")

youtube_url = st.text_input("Enter YouTube URL:")

if st.button("Get Video Title"):
    if youtube_url:
        output_filename = get_youtube_title(youtube_url)
        if output_filename:
            st.write(f"Video Title: {output_filename}")
    else:
        st.error("Please enter a YouTube URL.")

if st.button("Download Video"):
    if youtube_url:
        output_filename = get_youtube_title(youtube_url)
        if output_filename:
            download_youtube_video(youtube_url, output_filename)
    else:
        st.error("Please enter a YouTube URL.")
