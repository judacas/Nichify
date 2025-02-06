from typing import Dict, List
from dotenv import load_dotenv
from spotipy import Spotify # type: ignore
from spotipy.oauth2 import SpotifyOAuth # type: ignore
import os
import json

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-read-private, playlist-modify-private playlist-modify-public"
))

def get_all_playlist_tracks(playlist_id: str):
    tracks = []
    results = sp.playlist_tracks(playlist_id, limit=100)
    if results is None:
        raise ValueError("Playlist not found or empty.")
    while results:
        tracks.extend(results['items'])
        results = sp.next(results)

    return tracks

def find_exact_duplicates(playlist_id: str):
    # Fetch playlist tracks
    tracks = get_all_playlist_tracks(playlist_id)
    
    seen = {} # type: ignore

    for track in tracks:
        track_id: str = track['track']['id']
        title: str = track['track']['name']
        artist = ", ".join([a['name'] for a in track['track']['artists']]) if track['track']['artists'] else "Unknown Artist"
        length = track['track']['duration_ms']

        # Create a unique identifier
        track_key = (title, artist, length)

        if track_key in seen:
            seen[track_key].append(track_id)
        else:
            seen[track_key] = [track_id]

    return {key: value for key, value in seen.items() if len(value) > 1} # Return only the duplicates

def get_user_playlists() -> list[dict]:
    """
    Fetch playlists owned by the authenticated user, ensuring no duplicates.

    Returns:
        list[dict]: A list of playlists (name, id, description, tracks_total, snapshot_id, image_url).
    """
    playlists = []
    seen_ids = set()  # Track IDs we've already processed
    current_user_id = sp.current_user()
    if current_user_id is None:
        raise ValueError("User ID not found.")
    current_user_id = current_user_id['id']
    results = sp.current_user_playlists()

    while results:
        for playlist in results['items']:
            # Check if playlist ID has already been added
            if playlist['id'] not in seen_ids and playlist['owner']['id'] == current_user_id:
                playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'description': playlist.get('description', ''),
                    'tracks_total': playlist['tracks']['total'],
                    'snapshot_id': playlist['snapshot_id'],
                    'image_url': playlist['images'][0]['url'] if playlist['images'] else None
                })
                seen_ids.add(playlist['id'])  # Mark this ID as seen

        # Move to the next page of results
        results = sp.next(results) if results['next'] else None

    return playlists



if __name__ == "__main__":
    playlists = get_user_playlists()
    with open("user_playlists.json", "w", encoding="utf-8") as f:
        json.dump(playlists, f, indent=4, ensure_ascii=False)
    print("Playlists saved to 'user_playlists.json'.")


    