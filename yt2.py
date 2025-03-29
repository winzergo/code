import streamlit as st
import subprocess
import sys
from googleapiclient.discovery import build
import re
import requests

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Channel Video Title and Transcript Extractor')

# Check if the necessary packages are installed
try:
    from googleapiclient.discovery import build
except ImportError:
    st.warning("googleapiclient not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-api-python-client', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2'])
    from googleapiclient.discovery import build

channel_url = st.text_input('Enter YouTube Channel URL (e.g., https://www.youtube.com/@drmarkhyman):')
video_title = st.text_input('Enter Video Title:')

if channel_url and video_title:
    try:
        # Extract channel ID from the URL
        channel_id = re.search(r'@([\w\d_-]+)', channel_url).group(1)

        youtube = build('youtube', 'v3', developerKey=API_KEY)
        # Get channel details to find channel ID
        channel_response = youtube.search().list(
            part='snippet',
            type='channel',
            q=channel_id
        ).execute()

        channel_id = channel_response['items'][0]['id']['channelId']

        # Fetching the videos
        video_id = None
        next_page_token = None

        while True:
            playlist_response = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response['items']:
                if item['snippet']['title'] == video_title:
                    video_id = item['id']['videoId']
                    break

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token or video_id:
                break

        if video_id:
            st.write(f'Found video: {video_title} (ID: {video_id})')
            transcript_url = f'https://youtube-transcript-api.herokuapp.com/api/transcript/{video_id}'
            response = requests.get(transcript_url)

            if response.status_code == 200:
                transcript = response.json()
                st.write('Transcript:')
                for line in transcript:
                    st.write(line['text'])
            else:
                st.error('Transcript not available.')
        else:
            st.error('Video not found.')

    except Exception as e:
        st.error(f'Error: {str(e)}')
