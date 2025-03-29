import streamlit as st
from googleapiclient.discovery import build
import re

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Video Caption Checker (Using YouTube Data API v3)')

video_url1 = st.text_input('Enter First YouTube Video URL:')
video_url2 = st.text_input('Enter Second YouTube Video URL:')

def get_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

def check_captions(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.captions().list(part='snippet', videoId=video_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            captions = [item['snippet']['language'] for item in response['items']]
            return f'Captions available: {", ".join(captions)}'
        else:
            return 'No captions available for this video.'
    except Exception as e:
        return f'Error checking captions: {str(e)}'

for video_url in [video_url1, video_url2]:
    if video_url:
        video_id = get_video_id(video_url)
        if video_id:
            st.write(f'Video ID: {video_id}')
            caption_status = check_captions(video_id)
            st.write(caption_status)
        else:
            st.error('Invalid video URL. Please enter a valid YouTube link.')
