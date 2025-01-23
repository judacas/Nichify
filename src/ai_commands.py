from typing import Any, Callable, TypedDict
from spotify_handler import find_exact_duplicates, sp
from db_handler import playlists
from Levenshtein import ratio as levenshtein_ratio


def ai_call_remove_duplicates(
    playlist_id: str, include_similar: bool, remove_similar_automatically: bool
):
    try:
        exact_duplicates = find_exact_duplicates(playlist_id)
        if not exact_duplicates:
            return {"status": "Success", "message": "No duplicates found in the playlist."}
        sp.playlist_remove_all_occurrences_of_items(playlist_id, exact_duplicates)
        if include_similar:
            return {
                "status": "success",
                "message": f"Removed {len(exact_duplicates)} exact_duplicates",
                "removed": exact_duplicates,
                "Note": "Similar removal not implemented yet.",
            }
        return {
            "status": "success",
            "message": f"Removed {len(exact_duplicates)} exact_duplicates automatically.",
            "removed": exact_duplicates,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def ai_get_closest_playlist(title: str) -> dict:
    # Fetch relevant playlists

    if not playlists:
        return {"status": "error", "message": "No relevant playlists found, must edit some playlists in spotify to make them recent and restart nichify or provide direct link via share button in spotify."}

    user_input_lower = title.strip().lower()

    # 1. Check for exact match (case-insensitive)
    for playlist in playlists:
        if playlist.name.strip().lower() == user_input_lower:
            return {
                "status": "success",
                "playlist": {
                    "id": playlist.id,
                    "name": playlist.name,
                    "description": playlist.description,
                    "url": f"https://open.spotify.com/playlist/{playlist.id}"
                },
                "message": "Exact match found."
            }

    # 2. If no exact match, use Levenshtein ratio
    closest_match = playlists[0]
    highest_ratio:float = 0

    for playlist in playlists:
        similarity_ratio = levenshtein_ratio(user_input_lower, playlist.name.strip().lower())
        if similarity_ratio > highest_ratio:
            closest_match = playlist
            highest_ratio = similarity_ratio

    # Return details for the closest matching playlist
    return {
        "status": "success",
        "playlist": {
            "id": closest_match.id,
            "name": closest_match.name,
            "description": closest_match.description,
            "url": f"https://open.spotify.com/playlist/{closest_match.id}"
        },
        "message": f"Closest match found: {closest_match.name} (Similarity: {(highest_ratio * 100):.2f}%)",
        "recommendation": "Verify the playlist with the user before proceeding."
        
    }



def exit_application():
    print("\033[93mThank you for using Nichify! Exiting now.\033[0m")
    exit(0)

class CommandInfo(TypedDict):
    function: Callable[..., Any]
    menu_name: str
    
commands: dict[str, CommandInfo] = {
    "remove_duplicates": {
        "function": ai_call_remove_duplicates,
        "menu_name": "Remove Duplicates",
    },
    "exit_application": {
        "function": exit_application,
        "menu_name": "Exit Application"},
    "get_closest_playlist": {
        "function": ai_get_closest_playlist,
        "menu_name": "N/A",
    },
}
