import streamlit as st
import subprocess
import sys
from googleapiclient.discovery import build
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

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
            # Enhanced video ID extraction
            video_id = re.search(r'(?:v=|be/|embed/|youtu.be/|/v/|/e/|watch\?v=|&v=|youtu.be/|/embed/|/shorts/|/watch\?v=|/watch\?vi=)([\w\-]{11})', video_url)
            if video_id:
                video_id = video_id.group(1)
                st.write(f'Video ID: {video_id}')
            else:
                st.error('Invalid YouTube video URL format.')
                continue

            try:
                # Check if transcripts are available
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript(['en'])
                transcript_data = transcript.fetch()
                st.write('Transcript:')
                transcript_text = ' '.join([line['text'] for line in transcript_data])
                st.write(transcript_text)
            except TranscriptsDisabled:
                st.error('Transcripts are disabled for this video: ' + video_url)
            except NoTranscriptFound:
                st.error('No transcript found for this video: ' + video_url)
            except Exception as e:
                st.error(f'Transcript not available or not accessible for video: {video_url}. Reason: {str(e)}')

        except Exception as e:
            st.error(f'Error processing video {video_url}: {str(e)}')
