from typing import Any, List

from ai_commands import commands, exit_application
from ai_handler import process_ai_response
from constants import menu_prompt


def get_user_input(messages: List[Any]) -> List[Any]:
    while (user_input := input("\n\n\033[94mUser: ").strip()) == "":
        pass
    print("\033[0m")
    if user_input.strip().lower() in ["exit", "quit", "bye", "goodbye", "stop", "end", "leave", "close"]:
        exit_application()
    messages.append({"role": "user", "content": user_input})
    return messages

def process_user_request(messages: List[dict]) -> List[dict]:
    try:
        messages = get_user_input(messages)
    except ValueError as e:
        print("\n")
        return messages
    messages = process_ai_response(messages)
    return messages


def printMenu():
    print("\033[93mWelcome to Nichify!")
    print("You can ask me to do any of the below tasks:")
    for i, func_info in enumerate(commands.values(), 1):
        print(f"{i}. {func_info['menu_name']}")
    print("\033[0m")
    
def main():
    messages = [{"role": "system", "content": menu_prompt}]
    printMenu()
    while True:
        messages = process_user_request(messages)

if __name__ == "__main__":
    main()
    
    