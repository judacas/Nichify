from typing import Any, Callable, List
from ai_commands import (
    exit_application,
    ai_call_remove_duplicates,
    ai_get_closest_playlist,
)
from ai_handler import process_ai_response, process_user_request
from constants import menu_prompt
from db_handler import init_db, playlists
import json

with open("ai_tools/menu_tools.json", "r") as file:
    menuTools = json.load(file)

menuToolsMap: dict[str, Callable] = {
    "remove_duplicates": ai_call_remove_duplicates,
    "exit_application": exit_application,
    "get_closest_playlist": ai_get_closest_playlist,
}

def printMenu():
    print("\033[93mYou can ask me to do any of the below tasks:")
    options = ["Remove Duplicates", "Exit Application"]
    for option in options:
        print(f"\t• {option}")
    print("\033[0m")


def main():
    init_db()
    print("\033[93mWelcome to Nichify! I am your assistant for managing Spotify playlists.\033[0m")
    printMenu()
    messages = [{"role": "system", "content": menu_prompt}]
    while True:
        messages = process_user_request(messages, menuTools, menuToolsMap)


if __name__ == "__main__":
    main()
