import os
import json
from typing import Any, Callable, List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load function schemas from file
with open("tools.json", "r") as f:
    tools = json.load(f)

# Define the function implementations
def remove_duplicates(playlist_id, mode):
    return {
        "status": "success",
        "message": f"Removed duplicates from {playlist_id} in {mode} mode.",
    }

def combine_playlists(playlist_ids, method):
    return {
        "status": "success",
        "message": f"Combined playlists {playlist_ids} using method {method}.",
    }

def exit_application():
    print("\033[93mThank you for using Nichify! Exiting now.\033[0m")
    exit(0)

# Function dispatcher
functions: dict[str,Callable] = {
    "remove_duplicates": remove_duplicates,
    "combine_playlists": combine_playlists,
    "exit_application": exit_application,
}

def printMenu():
    print("\033[93mWelcome to Nichify!")
    print("You can ask me to do any of the below tasks:")
    for i, func_name in enumerate(functions.keys(), 1):
        print(f"{i}. {func_name}")
    print("\033[0m")


# System/Developer Prompt
system_prompt = """
You are Nichify, an assistant for managing Spotify playlists. Your available commands are your tools

- If a user requests a command that is not yet implemented, inform them and return to the menu.
- If a user requests anything unrelated, politely decline and bring them back to the menu.
- Always guide the user by showing the menu after completing their request.

Do not use markdown
"""



# Method 1: Get user input and add to messages
def get_user_input(messages: List[Any]) -> List[Any]:
    user_input = input("\n\033[94mUser: ")
    print("\033[0m")
    messages.append({"role": "user", "content": user_input})
    return messages

# Method 2: Handle function calls based on AI response
def handle_function_calls(response, messages: List[Any]) -> List[Any]:
    assistant_message = response.choices[0].message
    for tool_call in assistant_message.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        if func_name in functions:
            result = functions[func_name](**args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )
        else:
            raise ValueError(f"Function {func_name} not found in dispatcher.")
    messages = process_ai_response(messages)
    return messages

# Method 3: Call AI, handle function calls, and update messages
def process_ai_response(messages: List[Any]) -> List[Any]:
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools
    )
    if response.choices[0].finish_reason in ["length", "content_filter"]:
        raise ValueError(f"Model response is too long or filtered. \n{response.choices[0]}")

    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    # If the AI made function calls, handle them
    if response.choices[0].finish_reason == "tool_calls":
        messages = handle_function_calls(response, messages)

    return messages

# Method 4: Get user input and process AI response
def process_user_request(messages: List[dict]) -> List[dict]:
    messages = get_user_input(messages)
    messages = process_ai_response(messages)
    return messages

# Main loop
def main():
    printMenu()
    # Message list
    messages: Any = [{"role": "developer", "content": system_prompt}]
    while True:
        try:
            
            messages = process_user_request(messages)
            print(f"\n\033[92mAssistant: {messages[-1].content}\033[0m")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            exit_application()

if __name__ == "__main__":
    main()
