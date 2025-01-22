from dotenv import load_dotenv
from spotipy import Spotify # type: ignore
from spotipy.oauth2 import SpotifyOAuth # type: ignore
import os

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-read-private, playlist-modify-private playlist-modify-public"
))


def find_exact_duplicates(playlist_id: str):
    # Fetch playlist tracks
    results = sp.playlist_tracks(playlist_id)
    if not results:
        raise ValueError("Playlist not found or empty.")
    tracks = results['items']

    # Collect metadata for comparison
    seen = {}
    duplicates = []

    for track in tracks:
        track_id: str = track['track']['id']
        title: str = track['track']['name']
        artist = ", ".join([a['name'] for a in track['track']['artists']]) if track['track']['artists'] else "Unknown Artist"
        length = track['track']['duration_ms']

        # Create a unique identifier
        track_key = (title, artist, length)

        if track_key in seen:
            duplicates.append(track_id)
        else:
            seen[track_key] = track_id

    return duplicates

def combine_playlists(playlist_ids: list[str]):
    pass


    