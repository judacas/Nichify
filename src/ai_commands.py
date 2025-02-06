import json
import traceback
from spotify_handler import find_exact_duplicates, sp
from db_handler import playlists
from Levenshtein import ratio as levenshtein_ratio
from ai_handler import process_ai_response
from constants import find_playlist_prompt


def ai_call_remove_duplicates(
    playlist_id: str, include_similar: bool, remove_similar_automatically: bool
):
    try:
        exact_duplicates = find_exact_duplicates(playlist_id)
        if not exact_duplicates:
            return {
                "status": "Success",
                "message": "No duplicates found in the playlist.",
            }
        removed = list({track_id for track_ids in exact_duplicates.values() for track_id in track_ids})
        sp.playlist_remove_all_occurrences_of_items(playlist_id, removed)
        addBack = [track_ids[0] for track_ids in exact_duplicates.values()]
        sp.playlist_add_items(playlist_id, addBack)
        if include_similar:
            return {
                "status": "success",
                "message": f"Removed duplicates for {len(exact_duplicates)} songs",
                "removed": removed,
                "Note": "Similar removal not implemented yet.",
            }
        return {
            "status": "success",
            "message": f"Removed duplicates for {len(exact_duplicates)} song automatically.",
            "removed": removed,
        }
    except Exception as e:
        traceback_str = traceback.format_exc()
        return {"status": "error", "message": str(e), "traceback": traceback_str}


def ai_get_closest_playlist(description: str) -> dict:
    """
    Find the closest matching playlist based on user input using Levenshtein ratio.
    If no match is found, fallback to GPT-4o-mini.

    Args:
        title (str): The playlist name provided by the user.

    Returns:
        dict: A dictionary containing the matched playlist details or an error message.
    """
    if not playlists:
        return {
            "status": "error",
            "message": "No relevant playlists found. Please modify some playlists on Spotify and restart Nichify.",
        }

    user_input_lower = description.strip().lower()

    # 1. Check for exact match (case-insensitive)
    for playlist in playlists:
        if playlist.name.strip().lower() == user_input_lower:
            return {
                "status": "success",
                "playlist": {
                    "name": playlist.name,
                    "description": playlist.description,
                    "url": f"https://open.spotify.com/playlist/{playlist.id}",
                },
                "message": "Exact match found.",
            }

    # 2. Use Levenshtein ratio for fuzzy matching
    closest_match = playlists[0]
    highest_ratio: float = 0

    for playlist in playlists:
        similarity_ratio = levenshtein_ratio(
            user_input_lower, playlist.name.strip().lower()
        )
        if similarity_ratio > highest_ratio:
            closest_match = playlist
            highest_ratio = similarity_ratio

    if highest_ratio >= 0.7:  # Acceptable threshold for fuzzy matching
        return {
            "status": "success",
            "playlist": {
                "name": closest_match.name,
                "description": closest_match.description,
                "url": f"https://open.spotify.com/playlist/{closest_match.id}",
            },
            "message": f"Closest match found: {closest_match.name} (Similarity: {(highest_ratio * 100):.2f}%)",
        }

    # # 3. Fallback to GPT-4o-mini
    try:
        return find_closest_via_gpt(description)
    except Exception as e:
        return {"status": "error", "message": str(e)}

def find_closest_via_gpt(description):
    playlist_data = [
        {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "tracks_total": playlist.tracks_total
        }
        for playlist in playlists
    ]

    messages = [{"role": "system", "content": find_playlist_prompt}, {"role": "user", "content": f"target: {description}\n playlists: {json.dumps(playlist_data)}"}]
    messages = process_ai_response(messages)
    found = messages[-1]["content"]
    playlist = next((p for p in playlists if p.id == found), None)
    return (
        {
            "status": "success",
            "playlist": {
                "name": playlist.name,
                "description": playlist.description,
                "url": f"https://open.spotify.com/playlist/{playlist.id}",
            },
            "message": "Closest match found using GPT-4o-mini.",
        }
        if playlist
        else {
            "status": "error",
            "message": "No matching playlist found.",
            "AI_error": found,
        }
    )


def exit_application():
    print("\033[93mThank you for using Nichify! Exiting now.\033[0m")
    exit(0)
