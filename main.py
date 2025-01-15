import os
import json
from typing import Any
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
    print("Thank you for using Nichify! Exiting now.")
    exit(0)


# Function dispatcher
functions = {
    "remove_duplicates": remove_duplicates,
    "combine_playlists": combine_playlists,
    "exit_application": exit_application,
}

# System/Developer Prompt
system_prompt = """
You are Nichify, an assistant for managing Spotify playlists. Your available commands are your tools. You will start off by showing the menu of tools.

- If a user requests a command that is not yet implemented, inform them and return to the menu.
- If a user requests anything unrelated, politely decline and bring them back to the menu.
- Always guide the user by showing the menu after completing their request.

Do not use markdown
"""


# Main loop for handling user input
def main():

    messages: Any = [{"role": "developer", "content": system_prompt}]

    while True:
        # print(f"Messages: {messages}")
        # Call OpenAI API to interpret the user's input
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools
        )

        # Extract model response
        assistant_message = response.choices[0].message
        if response.choices[0].finish_reason == "length" or response.choices[0].finish_reason == "content_filter":
            raise ValueError(f"Model response is too long or filtered. \n{response.choices[0]} ")
        
        messages.append(assistant_message)
        
        if response.choices[0].finish_reason == "tool_calls":

            if assistant_message.tool_calls:
                # Handle tool calls
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
                        raise ValueError(
                            f"Function {func_name} not found in dispatcher."
                        )
                continue
                        
        else:
            print(f"Assistant: {assistant_message.content}")
        print("\n")
        user_input = input("\nYour request: ")
        messages.append({"role": "user", "content": user_input})


if __name__ == "__main__":
    main()
