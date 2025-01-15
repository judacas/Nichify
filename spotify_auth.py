import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Spotify authentication
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-read-private"
))

# Test the connection by fetching the current user's playlists
def test_spotify_connection():
    try:
        user = sp.current_user()
        print(f"Authenticated as: {user['display_name']}")

        playlists = sp.current_user_playlists(limit=5)
        print("\nUser Playlists:")
        for idx, playlist in enumerate(playlists['items']):
            print(f"{idx + 1}. {playlist['name']} (Tracks: {playlist['tracks']['total']})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_spotify_connection()
