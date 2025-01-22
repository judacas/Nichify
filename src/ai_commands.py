from typing import Any, Callable, TypedDict
from spotify_handler import find_exact_duplicates, sp


def ai_call_remove_duplicates(
    playlist_id: str, include_similar: bool, remove_similar_automatically: bool
):
    try:
        exact_duplicates = find_exact_duplicates(playlist_id)
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
}
