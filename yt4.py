import streamlit as st
import subprocess
import sys
from googleapiclient.discovery import build
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Video Transcript Extractor (Two Videos)')

# Check if the necessary packages are installed
try:
    from googleapiclient.discovery import build
except ImportError:
    st.warning("googleapiclient not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-api-python-client', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2', 'youtube-transcript-api'])
    from googleapiclient.discovery import build

video_url1 = st.text_input('Enter First YouTube Video URL (e.g., https://www.youtube.com/watch?v=EHs5ghjeB5k):')
video_url2 = st.text_input('Enter Second YouTube Video URL (e.g., https://www.youtube.com/watch?v=EHs5ghjeB5k):')

for video_url in [video_url1, video_url2]:
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
                st.error('Transcript not available or not accessible for video: ' + video_url)

        except Exception as e:
            st.error(f'Error processing video {video_url}: {str(e)}')
