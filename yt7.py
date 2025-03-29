import streamlit as st
from googleapiclient.discovery import build
import re

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Channel Video Title Extractor (All Videos)')

channel_url = st.text_input('Enter YouTube Channel URL (e.g., https://www.youtube.com/@drmarkhyman):')

def get_channel_id(url):
    # Extract channel ID from URL using YouTube Data API
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        channel_name = re.search(r'@([\w\d_-]+)', url).group(1)
        request = youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel',
            maxResults=1
        )
        response = request.execute()
        return response['items'][0]['snippet']['channelId']
    except Exception as e:
        st.error(f"Error retrieving channel ID: {e}")
        return None

def get_all_videos(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            order='date'
        )
        response = request.execute()

        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['id'].get('videoId')
            if video_id:
                videos.append((video_title, f"https://www.youtube.com/watch?v={video_id}"))

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

if channel_url:
    channel_id = get_channel_id(channel_url)
    if channel_id:
        st.write(f"Channel ID: {channel_id}")
        videos = get_all_videos(channel_id)
        if videos:
            st.write(f"Total videos found: {len(videos)}")
            for title, link in videos:
                st.write(f"{title} - {link}")
        else:
            st.error("No videos found.")
