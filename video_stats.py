import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

api_key = os.getenv("API_KEY")
channel_handle = "MrBeast"
maxResults = 50

def get_playlist_id(channel_handle, api_key):
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_items = data["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(f"Channel Playlist ID for {channel_handle}: {channel_playlist_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        return None
    return channel_playlist_id

def get_video_ids(playlistId, api_key):

    video_ids = []

    pageToken = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={api_key}"

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            video_ids.extend([item["contentDetails"]["videoId"] for item in data["items"]])

            pageToken = data.get("nextPageToken")
            if not pageToken:
                break

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        return None

    return video_ids

if __name__ == "__main__":
    playlistId = get_playlist_id(channel_handle, api_key)
    get_video_ids(playlistId, api_key)
    
