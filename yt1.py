import streamlit as st
from googleapiclient.discovery import build
import re

API_KEY = 'YOUR_YOUTUBE_API_KEY'

st.title('YouTube Channel Video Title Extractor')

channel_url = st.text_input('Enter YouTube Channel URL (e.g., https://www.youtube.com/@drmarkhyman):')

if channel_url:
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
        video_titles = []
        next_page_token = None

        while True:
            playlist_response = youtube.search().list(
                part='snippet',
                channelId=channel_id,
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
