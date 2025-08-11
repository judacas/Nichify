from types import SimpleNamespace
from src.ai_handler import process_ai_response


class DummyClient:
    def __init__(self, chunks):
        self._chunks = chunks

    def chat(self):  # pragma: no cover - interface adapter
        return self

    class completions:
        @staticmethod
        def create(model, messages, stream=True, tools=None):
            return []


def make_chunk(content=None, tool_index=None, arg_piece=None, finish_reason=None):
    delta = SimpleNamespace(content=content, tool_calls=None)
    if tool_index is not None:
        function = SimpleNamespace(name="remove_duplicates", arguments=arg_piece)
        tool_call = SimpleNamespace(index=tool_index, function=function, id="call-0")
        delta.tool_calls = [tool_call]
    choice = SimpleNamespace(delta=delta, finish_reason=finish_reason)
    return SimpleNamespace(choices=[choice])


def test_stream_argument_assembly(monkeypatch):
    # Create chunks that deliver tool arguments in pieces
    chunks = [
        make_chunk(content="Working on it..."),
        make_chunk(tool_index=0, arg_piece="{\"playlist_id\":"),
        make_chunk(tool_index=0, arg_piece="\"abc\","),
        make_chunk(tool_index=0, arg_piece="\"include_similar\":false,\"remove_similar_automatically\":false}"),
        make_chunk(finish_reason=None),
    ]

    class MockClient:
        class chat:
            class completions:
                @staticmethod
                def create(model, messages, stream=True, tools=None):
                    for c in chunks:
                        yield c

    # Patch ai_handler.client used by process_ai_response
    import src.ai_handler as ai_handler

    old_client = ai_handler.client
    ai_handler.client = MockClient()  # type: ignore
    try:
        # Provide tools so that tool call path is taken
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "remove_duplicates",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            }
        ]
        # Minimal toolsMap to avoid execution; patch to capture args
        captured = {}

        def fake_tool(**kwargs):
            captured.update(kwargs)
            return {"status": "ok"}

        messages = [{"role": "system", "content": "x"}]
        messages = process_ai_response(messages, tools=tools, toolsMap={"remove_duplicates": fake_tool})
        assert captured["playlist_id"] == "abc"
        assert captured["include_similar"] is False
        assert captured["remove_similar_automatically"] is False
    finally:
        ai_handler.client = old_client