import streamlit as st
import subprocess
import sys
import re
from googleapiclient.discovery import build

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'  # Replace with your API key

st.title('YouTube Channel Video Title Extractor')

# Ensure the required packages are installed
try:
    from googleapiclient.discovery import build
except ImportError:
    st.warning("googleapiclient not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                             'google-api-python-client', 'google-auth', 
                             'google-auth-oauthlib', 'google-auth-httplib2'])
    from googleapiclient.discovery import build

channel_url = st.text_input('Enter YouTube Channel URL (e.g., https://www.youtube.com/@drmarkhyman):')

if channel_url:
    try:
        # Extract the channel handle (e.g., drmarkhyman) from the URL
        channel_handle = re.search(r'@([\w\d_-]+)', channel_url).group(1)

        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        # Search for the channel using its handle to retrieve the channel ID
        search_response = youtube.search().list(
            part='snippet',
            q=channel_handle,
            type='channel',
            maxResults=1
        ).execute()

        channel_id = search_response['items'][0]['id']['channelId']

        # Retrieve the channel details to get the uploads playlist ID
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Fetch all videos from the uploads playlist
        video_titles = []
        next_page_token = None

        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response['items']:
                video_titles.append(item['snippet']['title'])

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        st.write(f'Found {len(video_titles)} videos:')
        for title in video_titles:
            st.write(title)

    except Exception as e:
        st.error(f'Error: {str(e)}')
