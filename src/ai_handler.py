import os
from typing import Any, List
import json
from openai import OpenAI
from dotenv import load_dotenv
from ai_commands import commands

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load function schemas from file
with open(os.path.join("..", "tools.json"), "r") as f:
    tools = json.load(f)

def handle_function_calls(tool_calls, messages: List[Any]) -> List[Any]:
    for tool_call in tool_calls:
        command = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(commands)
        if command in commands:
            result = commands[command]["function"](**args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )
        else:
            raise ValueError(f"Command {command} not found in dispatcher.")
    messages = process_ai_response(messages)
    return messages

def process_ai_response(messages: List[Any]) -> List[Any]:
    stream = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools, stream=True
    )
    final_tool_calls = {}
    final_content = ""
    first_flag = True
    for chunk in stream:
        if chunk.choices[0].finish_reason in ["length", "content_filter"]:
            raise ValueError(f"Model response is too long or filtered. \n{chunk.choices[0]}")
        delta = chunk.choices[0].delta
        if delta.content:
            if first_flag:
                first_flag = False
                print("\n\033[92mAssistant: \033[0m", end="")
            print(f"\033[92m{delta.content}\033[0m", end="")
            final_content += delta.content
        if delta.tool_calls:
            for tool_call in delta.tool_calls:
                index = tool_call.index

                if index not in final_tool_calls:
                    final_tool_calls[index] = tool_call

                final_tool_calls[index].function.arguments += tool_call.function.arguments  # type: ignore
    
    if final_content:
        messages.append({"role": "assistant", "content": final_content})
        
    if final_tool_calls:
        messages.append({"role": "assistant", "tool_calls": list(final_tool_calls.values())})
        messages = handle_function_calls(list(final_tool_calls.values()), messages)

    return messages