from unittest.mock import MagicMock, call

import pytest
from slack_sdk.web.chat_stream import ChatStream

from slack_bolt.agent.tools import Tools, ToolDefinition, _introspect_handler


# ---- Helpers ----


def _make_stream():
    stream = MagicMock(spec=ChatStream)
    stream.append.return_value = None
    return stream


def _simple_handler(query: str, limit: int = 10) -> str:
    """Search for something."""
    return f"{query}:{limit}"


# ======================================================================
# add()
# ======================================================================


class TestAdd:
    def test_decorator_usage(self):
        tools = Tools()

        @tools.add("search")
        def search(query: str) -> str:
            """Find stuff."""
            return query

        assert "search" in tools
        assert len(tools) == 1

    def test_programmatic_usage(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler, description="Search")
        assert "search" in tools

    def test_duplicate_name_raises(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)
        with pytest.raises(ValueError, match="already registered"):
            tools.add("search", handler=_simple_handler)

    def test_docstring_as_description(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)
        defn = tools._definitions["search"]
        assert defn.description == "Search for something."

    def test_explicit_description_overrides_docstring(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler, description="Custom desc")
        assert tools._definitions["search"].description == "Custom desc"

    def test_explicit_parameters_override_introspection(self):
        tools = Tools()
        custom_params = {"q": {"type": "string"}}
        tools.add("search", handler=_simple_handler, parameters=custom_params)
        assert tools._definitions["search"].parameters == custom_params

    def test_explicit_required_override_introspection(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler, required=["query", "limit"])
        assert tools._definitions["search"].required == ["query", "limit"]

    def test_decorator_returns_original_function(self):
        tools = Tools()

        @tools.add("search")
        def search(query: str) -> str:
            return query

        assert callable(search)
        assert search("hello") == "hello"

    def test_programmatic_returns_none(self):
        tools = Tools()
        result = tools.add("search", handler=_simple_handler)
        assert result is None


# ======================================================================
# _introspect_handler
# ======================================================================


class TestIntrospection:
    def test_str_type(self):
        def fn(x: str):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "string"

    def test_int_type(self):
        def fn(x: int):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "integer"

    def test_float_type(self):
        def fn(x: float):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "number"

    def test_bool_type(self):
        def fn(x: bool):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "boolean"

    def test_list_type(self):
        def fn(x: list):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "array"

    def test_dict_type(self):
        def fn(x: dict):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "object"

    def test_no_type_hint_defaults_to_string(self):
        def fn(x):
            pass

        info = _introspect_handler(fn)
        assert info["parameters"]["x"]["type"] == "string"

    def test_required_vs_optional(self):
        def fn(a: str, b: int = 5):
            pass

        info = _introspect_handler(fn)
        assert "a" in info["required"]
        assert "b" not in info["required"]

    def test_docstring_used_as_description(self):
        def fn():
            """Do something cool."""
            pass

        info = _introspect_handler(fn)
        assert info["description"] == "Do something cool."

    def test_no_docstring(self):
        def fn():
            pass

        info = _introspect_handler(fn)
        assert info["description"] == ""


# ======================================================================
# execute()
# ======================================================================


class TestExecute:
    def test_status_lifecycle(self):
        tools = Tools()
        tools.add("echo", handler=lambda msg: msg)

        stream = _make_stream()
        result = tools.execute(stream, call_id="c1", name="echo", arguments={"msg": "hi"})

        assert result == "hi"
        assert stream.append.call_count == 2
        calls = stream.append.call_args_list
        assert calls[0] == call(markdown_text="", task_update={"call_id": "c1", "status": "in_progress"})
        assert calls[1] == call(markdown_text="", task_update={"call_id": "c1", "status": "completed", "output": "hi"})

    def test_unknown_tool_raises_keyerror(self):
        tools = Tools()
        stream = _make_stream()
        with pytest.raises(KeyError, match="Unknown tool"):
            tools.execute(stream, call_id="c1", name="nope")

    def test_handler_exception_sends_failed_then_reraises(self):
        def bad_handler():
            raise RuntimeError("boom")

        tools = Tools()
        tools.add("bad", handler=bad_handler)
        stream = _make_stream()

        with pytest.raises(RuntimeError, match="boom"):
            tools.execute(stream, call_id="c1", name="bad")

        calls = stream.append.call_args_list
        assert len(calls) == 2
        assert calls[0] == call(markdown_text="", task_update={"call_id": "c1", "status": "in_progress"})
        assert calls[1] == call(markdown_text="", task_update={"call_id": "c1", "status": "failed", "output": "boom"})

    def test_arguments_forwarded_correctly(self):
        captured = {}

        def handler(a: str, b: int = 0):
            captured["a"] = a
            captured["b"] = b
            return "ok"

        tools = Tools()
        tools.add("fn", handler=handler)
        stream = _make_stream()
        tools.execute(stream, call_id="c1", name="fn", arguments={"a": "hello", "b": 42})

        assert captured == {"a": "hello", "b": 42}

    def test_result_returned(self):
        tools = Tools()
        tools.add("add", handler=lambda x, y: str(int(x) + int(y)))
        stream = _make_stream()
        result = tools.execute(stream, call_id="c1", name="add", arguments={"x": "3", "y": "4"})
        assert result == "7"

    def test_none_arguments_treated_as_empty(self):
        tools = Tools()
        tools.add("noop", handler=lambda: "done")
        stream = _make_stream()
        result = tools.execute(stream, call_id="c1", name="noop", arguments=None)
        assert result == "done"


# ======================================================================
# schema()
# ======================================================================


class TestSchema:
    def test_openai_format(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)

        schemas = tools.schema("openai")
        assert len(schemas) == 1
        s = schemas[0]
        assert s["type"] == "function"
        assert s["function"]["name"] == "search"
        assert s["function"]["description"] == "Search for something."
        params = s["function"]["parameters"]
        assert params["type"] == "object"
        assert "query" in params["properties"]
        assert "limit" in params["properties"]
        assert params["required"] == ["query"]

    def test_anthropic_format(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)

        schemas = tools.schema("anthropic")
        assert len(schemas) == 1
        s = schemas[0]
        assert s["name"] == "search"
        assert s["description"] == "Search for something."
        assert "input_schema" in s
        assert s["input_schema"]["type"] == "object"
        assert "query" in s["input_schema"]["properties"]
        assert s["input_schema"]["required"] == ["query"]

    def test_unsupported_provider_raises(self):
        tools = Tools()
        with pytest.raises(ValueError, match="Unsupported provider"):
            tools.schema("gemini")

    def test_empty_registry(self):
        tools = Tools()
        assert tools.schema("openai") == []
        assert tools.schema("anthropic") == []

    def test_multiple_tools(self):
        tools = Tools()
        tools.add("a", handler=lambda: "x")
        tools.add("b", handler=lambda: "y")

        schemas = tools.schema("openai")
        assert len(schemas) == 2
        names = {s["function"]["name"] for s in schemas}
        assert names == {"a", "b"}


# ======================================================================
# copy()
# ======================================================================


class TestCopy:
    def test_independent_registry(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)
        cloned = tools.copy()

        cloned.add("other", handler=lambda: "x")
        assert "other" in cloned
        assert "other" not in tools

    def test_shared_handler_references(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)
        cloned = tools.copy()

        assert tools._definitions["search"].handler is cloned._definitions["search"].handler

    def test_deep_copied_parameters(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)
        cloned = tools.copy()

        cloned._definitions["search"].parameters["query"]["type"] = "integer"
        assert tools._definitions["search"].parameters["query"]["type"] == "string"


# ======================================================================
# __len__ / __contains__
# ======================================================================


class TestConvenience:
    def test_len_empty(self):
        assert len(Tools()) == 0

    def test_len_with_tools(self):
        tools = Tools()
        tools.add("a", handler=lambda: "x")
        tools.add("b", handler=lambda: "y")
        assert len(tools) == 2

    def test_contains_true(self):
        tools = Tools()
        tools.add("search", handler=_simple_handler)
        assert "search" in tools

    def test_contains_false(self):
        tools = Tools()
        assert "search" not in tools


# ======================================================================
# Import paths
# ======================================================================


class TestImports:
    def test_import_from_agent_module(self):
        from slack_bolt.agent import Tools as ImportedTools

        assert ImportedTools is Tools

    def test_import_from_slack_bolt(self):
        from slack_bolt import Tools as ImportedTools

        assert ImportedTools is Tools
