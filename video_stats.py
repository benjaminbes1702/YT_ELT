import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

api_key = os.getenv("API_KEY")
channel_handle = "MrBeast"

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

if __name__ == "__main__":
    get_playlist_id(channel_handle, api_key)
