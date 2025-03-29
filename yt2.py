import streamlit as st
import subprocess
import sys
from googleapiclient.discovery import build
import re
import requests

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Video Transcript Extractor')

# Check if the necessary packages are installed
try:
    from googleapiclient.discovery import build
except ImportError:
    st.warning("googleapiclient not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-api-python-client', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2'])
    from googleapiclient.discovery import build

video_url = st.text_input('Enter YouTube Video URL (e.g., https://www.youtube.com/watch?v=EHs5ghjeB5k):')

if video_url:
    try:
        # Extract video ID from the URL
        video_id = re.search(r'v=([\w\d_-]+)', video_url).group(1)
        st.write(f'Video ID: {video_id}')

        transcript_url = f'https://youtube-transcript-api.herokuapp.com/api/transcript/{video_id}'
        response = requests.get(transcript_url)

        if response.status_code == 200:
            transcript = response.json()
            st.write('Transcript:')
            for line in transcript:
                st.write(line['text'])
        else:
            st.error('Transcript not available.')

    except Exception as e:
        st.error(f'Error: {str(e)}')
