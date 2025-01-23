import os
from typing import Any, Callable, List, Optional
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_user_input(messages: List[Any]) -> List[Any]:
    while (user_input := input("\n\n\033[94mUser: ").strip()) == "":
        pass
    print("\033[0m")
    if user_input.strip().lower() in [
        "exit",
        "quit",
        "bye",
        "goodbye",
        "stop",
        "end",
        "leave",
        "close",
    ]:
        print("\033[93mThank you for using Nichify! Exiting now.\033[0m")
        exit(0)
    messages.append({"role": "user", "content": user_input})
    return messages


def process_user_request(
    messages: List[Any],
    tools: Optional[dict] = None,
    toolsMap: Optional[dict[str, Callable[..., Any]]] = None,
) -> List[dict]:
    try:
        messages = get_user_input(messages)
    except ValueError as e:
        print("\n")
        return messages
    messages = process_ai_response(messages, tools=tools, toolsMap=toolsMap)
    return messages


def handle_function_calls(
    tool_calls,
    messages: List[Any],
    tools: dict,
    toolsMap: dict[str, Callable[..., Any]],
) -> List[Any]:
    for tool_call in tool_calls:
        tool = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"\n\033[94mTool: {tool}({args})\033[0m")
        if tool not in toolsMap:
            raise ValueError(f"Command {tool} not found in dispatcher.")
        result:dict = toolsMap[tool](**args)
        print(f"\033[94mResult: {json.dumps(result, indent=4)}\033[0m")
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )
    messages = process_ai_response(messages, tools, toolsMap)
    return messages


def process_ai_response(
    messages: List[Any],
    tools: Optional[dict] = None,
    toolsMap: Optional[dict[str, Callable[..., Any]]] = None,
) -> List[Any]:
    if bool(tools) != bool(toolsMap):
        raise ValueError("Both tools and toolsMap must be provided or omitted.")

    stream = (
        client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools, stream=True
        )
        if tools
        else client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, stream=True
        )
    )
    final_tool_calls = {}
    final_content = ""
    first_flag = True
    for chunk in stream:
        if chunk.choices[0].finish_reason in ["length", "content_filter"]:
            raise ValueError(
                f"Model response is too long or filtered. \n{chunk.choices[0]}"
            )
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

    if final_tool_calls and tools and toolsMap:
        messages.append(
            {"role": "assistant", "tool_calls": list(final_tool_calls.values())}
        )
        messages = handle_function_calls(
            list(final_tool_calls.values()), messages, tools, toolsMap
        )

    return messages
