import streamlit as st
import subprocess
import sys
from googleapiclient.discovery import build
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Video Transcript Extractor (No Line Breaks)')

# Check if the necessary packages are installed
try:
    from googleapiclient.discovery import build
except ImportError:
    st.warning("googleapiclient not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-api-python-client', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2', 'youtube-transcript-api'])
    from googleapiclient.discovery import build

video_url = st.text_input('Enter YouTube Video URL (e.g., https://www.youtube.com/watch?v=EHs5ghjeB5k):')

if video_url:
    try:
        # Extract video ID from the URL
        video_id = re.search(r'v=([\w\d_-]+)', video_url).group(1)
        st.write(f'Video ID: {video_id}')

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            st.write('Transcript:')
            transcript_text = ' '.join([line['text'] for line in transcript])
            st.write(transcript_text)
        except Exception as e:
            st.error('Transcript not available or not accessible.')

    except Exception as e:
        st.error(f'Error: {str(e)}')
