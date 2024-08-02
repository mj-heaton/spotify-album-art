import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from dotenv import load_dotenv


load_dotenv()

# Set your Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:8888/callback/'

# Scope required to read user's playlists
scope = 'playlist-read-private'

# Create an instance of the SpotifyOAuth class
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Fetch current user's playlists
playlists = sp.current_user_playlists()

# Create a directory to save cover photos
if not os.path.exists('playlist_covers'):
    os.makedirs('playlist_covers')

# Function to download image from a URL
def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)

# Loop through each playlist and download the cover photo
for playlist in playlists['items']:
    print(f"Processing playlist: {playlist['name']}")
    playlist_name = playlist['name']
    playlist_id = playlist['id']
    cover_image_url = playlist['images'][0]['url']  # Get the cover image URL

    # Define the file path to save the cover image
    file_path = os.path.join('playlist_covers', f"{playlist_name}.jpg")

    # Download and save the cover image
    download_image(cover_image_url, file_path)
    print(f"Downloaded cover photo for playlist: {playlist_name}")

print("All cover photos have been downloaded successfully.")
