import streamlit as st
import subprocess
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

# Import and install the YouTube API client if needed
try:
    from googleapiclient.discovery import build
except ImportError:
    st.warning("googleapiclient not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                             'google-api-python-client', 'google-auth', 
                             'google-auth-oauthlib', 'google-auth-httplib2', 
                             'youtube-transcript-api'])
    from googleapiclient.discovery import build

API_KEY = 'AIzaSyA23ZOgNrv1CrIHE8Ckma3Hc5y0jZ9Xkuw'

st.title('YouTube Video Transcript Extractor (No Line Breaks)')

# Input fields for channel URL and video title
channel_url = st.text_input('Enter YouTube Channel URL (e.g., https://www.youtube.com/channel/UCxxx, https://www.youtube.com/@username, or https://www.youtube.com/c/CustomName):')
video_title_input = st.text_input('Enter the YouTube Video Title:')

if channel_url and video_title_input:
    try:
        channel_id = None
        # Extract the channel ID based on the URL format
        if "channel" in channel_url:
            channel_id = re.search(r'/channel/([\w\d_-]+)', channel_url).group(1)
        elif "user" in channel_url:
            username = re.search(r'/user/([\w\d_-]+)', channel_url).group(1)
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            response = youtube.channels().list(forUsername=username, part='id').execute()
            if response['items']:
                channel_id = response['items'][0]['id']
            else:
                st.error("Channel not found for given username.")
        elif "/c/" in channel_url:
            custom_name = re.search(r'/c/([\w\d_-]+)', channel_url).group(1)
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            search_response = youtube.search().list(
                q=custom_name, type='channel', part='snippet', maxResults=1
            ).execute()
            if search_response['items']:
                channel_id = search_response['items'][0]['id']['channelId']
            else:
                st.error("Channel not found for given custom URL.")
        elif "@" in channel_url:
            # Handle URLs like https://www.youtube.com/@drmarkhyman/videos
            handle = re.search(r'@([\w\d_-]+)', channel_url).group(1)
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            search_response = youtube.search().list(
                q=handle, type='channel', part='snippet', maxResults=1
            ).execute()
            if search_response['items']:
                channel_id = search_response['items'][0]['id']['channelId']
            else:
                st.error("Channel not found for given handle URL.")
        else:
            st.error("Invalid channel URL format.")

        if channel_id:
            st.write(f'Channel ID: {channel_id}')
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            # Search for videos on the channel that match the provided title
            search_response = youtube.search().list(
                channelId=channel_id,
                q=video_title_input,
                type='video',
                part='id,snippet',
                maxResults=5
            ).execute()

            if search_response['items']:
                # Select the first matching video (optionally, refine the matching further)
                video_item = search_response['items'][0]
                video_id = video_item['id']['videoId']
                st.write(f"Video found: {video_item['snippet']['title']} (ID: {video_id})")
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    transcript_text = ' '.join([line['text'] for line in transcript])
                    st.write('Transcript:')
                    st.write(transcript_text)
                except Exception as e:
                    st.error("Transcript not available or not accessible.")
            else:
                st.error("No videos found with the given title on this channel.")
    except Exception as e:
        st.error(f'Error: {str(e)}')
