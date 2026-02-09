from time import sleep
from typing import Optional

from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest
from slack_bolt.context.agent.agent_utilities import AgentUtilities
from slack_bolt.context.agent.mcp import SlackMCPServer
from slack_bolt.context.agent.tool_registry import (
    AgentToolRegistry,
    ToolDefinition,
    _introspect_parameters,
)
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestToolRegistry:
    """Unit tests for AgentToolRegistry, ToolDefinition, and schema generation."""

    def test_register_tool_with_explicit_params(self):
        registry = AgentToolRegistry()
        registry.add(
            "search",
            lambda query: f"results for {query}",
            description="Search for documents",
            parameters={"query": {"type": "string", "description": "Search query"}},
            required=["query"],
        )
        assert "search" in registry._tools
        assert registry._tools["search"].description == "Search for documents"
        assert registry._tools["search"].parameters == {"query": {"type": "string", "description": "Search query"}}
        assert registry._tools["search"].required == ["query"]

    def test_register_tool_with_introspection(self):
        def search_docs(query: str, limit: int = 10) -> str:
            """Search company documentation."""
            return f"results for {query}"

        registry = AgentToolRegistry()
        tool_def = registry.add("search_docs", search_docs)

        assert tool_def.name == "search_docs"
        assert tool_def.description == "Search company documentation."
        assert "query" in tool_def.parameters
        assert tool_def.parameters["query"]["type"] == "string"
        assert "limit" in tool_def.parameters
        assert tool_def.parameters["limit"]["type"] == "integer"
        assert "query" in tool_def.required
        assert "limit" not in tool_def.required  # has default

    def test_introspect_parameters(self):
        def my_func(name: str, count: int, ratio: float, active: bool, tags: list, data: dict):
            pass

        props, req = _introspect_parameters(my_func)
        assert props["name"]["type"] == "string"
        assert props["count"]["type"] == "integer"
        assert props["ratio"]["type"] == "number"
        assert props["active"]["type"] == "boolean"
        assert props["tags"]["type"] == "array"
        assert props["data"]["type"] == "object"
        assert set(req) == {"name", "count", "ratio", "active", "tags", "data"}

    def test_introspect_parameters_with_defaults(self):
        def my_func(required_param: str, optional_param: str = "default"):
            pass

        props, req = _introspect_parameters(my_func)
        assert "required_param" in req
        assert "optional_param" not in req

    def test_openai_schema(self):
        registry = AgentToolRegistry()
        registry.add(
            "search_confluence",
            lambda query: "results",
            description="Search company docs",
            parameters={"query": {"type": "string", "description": "Search query"}},
            required=["query"],
        )
        schemas = registry.schema("openai")
        assert len(schemas) == 1
        schema = schemas[0]
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "search_confluence"
        assert schema["function"]["description"] == "Search company docs"
        assert schema["function"]["parameters"]["type"] == "object"
        assert "query" in schema["function"]["parameters"]["properties"]
        assert schema["function"]["parameters"]["required"] == ["query"]

    def test_anthropic_schema(self):
        registry = AgentToolRegistry()
        registry.add(
            "search_confluence",
            lambda query: "results",
            description="Search company docs",
            parameters={"query": {"type": "string", "description": "Search query"}},
            required=["query"],
        )
        schemas = registry.schema("anthropic")
        assert len(schemas) == 1
        schema = schemas[0]
        assert schema["name"] == "search_confluence"
        assert schema["description"] == "Search company docs"
        assert schema["input_schema"]["type"] == "object"
        assert "query" in schema["input_schema"]["properties"]
        assert schema["input_schema"]["required"] == ["query"]

    def test_schema_invalid_provider(self):
        registry = AgentToolRegistry()
        try:
            registry.schema("gemini")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "gemini" in str(e)

    def test_tool_definition_openai_schema(self):
        tool = ToolDefinition(
            name="test",
            description="Test tool",
            parameters={"arg": {"type": "string"}},
            required=["arg"],
            handler=lambda arg: arg,
        )
        schema = tool.to_openai_schema()
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "test"

    def test_tool_definition_anthropic_schema(self):
        tool = ToolDefinition(
            name="test",
            description="Test tool",
            parameters={"arg": {"type": "string"}},
            required=["arg"],
            handler=lambda arg: arg,
        )
        schema = tool.to_anthropic_schema()
        assert schema["name"] == "test"
        assert schema["input_schema"]["type"] == "object"

    def test_execute_tool(self):
        registry = AgentToolRegistry()
        registry.add(
            "greet",
            lambda name: f"Hello, {name}!",
            description="Greet someone",
            parameters={"name": {"type": "string"}},
            required=["name"],
        )

        class MockStreamer:
            def __init__(self):
                self.updates = []

            def append(self, **kwargs):
                self.updates.append(kwargs)

        streamer = MockStreamer()
        result = registry.execute(streamer, "call_123", "greet", {"name": "World"})
        assert result == "Hello, World!"

        # Check status updates were sent
        assert len(streamer.updates) == 2
        assert streamer.updates[0]["task_update"]["status"] == "in_progress"
        assert streamer.updates[1]["task_update"]["status"] == "completed"

    def test_execute_tool_with_title(self):
        registry = AgentToolRegistry()
        registry.add(
            "search",
            lambda query: "results",
            description="Search",
            parameters={"query": {"type": "string"}},
            required=["query"],
            title="Searching...",
        )

        class MockStreamer:
            def __init__(self):
                self.updates = []

            def append(self, **kwargs):
                self.updates.append(kwargs)

        streamer = MockStreamer()
        registry.execute(streamer, "call_1", "search", {"query": "test"})
        assert streamer.updates[0]["task_update"]["title"] == "Searching..."

    def test_execute_tool_not_found(self):
        registry = AgentToolRegistry()

        class MockStreamer:
            def append(self, **kwargs):
                pass

        try:
            registry.execute(MockStreamer(), "call_1", "nonexistent", {})
            assert False, "Should have raised KeyError"
        except KeyError:
            pass

    def test_execute_tool_failure_sends_failed_status(self):
        def failing_tool():
            raise RuntimeError("Tool failed")

        registry = AgentToolRegistry()
        registry.add(
            "failing",
            failing_tool,
            description="A tool that fails",
            parameters={},
            required=[],
        )

        class MockStreamer:
            def __init__(self):
                self.updates = []

            def append(self, **kwargs):
                self.updates.append(kwargs)

        streamer = MockStreamer()
        try:
            registry.execute(streamer, "call_1", "failing", {})
            assert False, "Should have raised RuntimeError"
        except RuntimeError:
            pass

        assert len(streamer.updates) == 2
        assert streamer.updates[0]["task_update"]["status"] == "in_progress"
        assert streamer.updates[1]["task_update"]["status"] == "failed"

    def test_add_tool_definition(self):
        registry = AgentToolRegistry()
        tool_def = ToolDefinition(
            name="my_tool",
            description="A tool",
            parameters={},
            required=[],
            handler=lambda: "result",
        )
        registry.add(tool_def)
        assert "my_tool" in registry._tools

    def test_add_mcp_server(self):
        registry = AgentToolRegistry()
        mcp = SlackMCPServer("xoxb-token")
        registry.add(mcp)
        assert len(registry._mcp_servers) == 1

    def test_add_invalid_type(self):
        registry = AgentToolRegistry()
        try:
            registry.add(12345)
            assert False, "Should have raised TypeError"
        except TypeError as e:
            assert "int" in str(e)

    def test_add_with_name_and_handler(self):
        def greet(name: str) -> str:
            """Say hello."""
            return f"Hello, {name}!"

        registry = AgentToolRegistry()
        tool_def = registry.add("greet", greet)
        assert tool_def is not None
        assert tool_def.name == "greet"
        assert tool_def.description == "Say hello."
        assert "greet" in registry._tools

    def test_add_name_without_handler_raises(self):
        registry = AgentToolRegistry()
        try:
            registry.add("my_tool")
            assert False, "Should have raised TypeError"
        except TypeError as e:
            assert "handler is required" in str(e)

    def test_add_handler_with_mcp_raises(self):
        registry = AgentToolRegistry()
        try:
            registry.add(SlackMCPServer("xoxb-token"), lambda: "nope")
            assert False, "Should have raised TypeError"
        except TypeError as e:
            assert "handler cannot be provided" in str(e)

    def test_copy_isolation(self):
        registry = AgentToolRegistry()
        registry.add(
            "global_tool",
            lambda: "result",
            description="A global tool",
            parameters={},
            required=[],
        )

        copied = registry.copy()
        copied.add(
            "local_tool",
            lambda: "local result",
            description="A local tool",
            parameters={},
            required=[],
        )

        assert "global_tool" in copied._tools
        assert "local_tool" in copied._tools
        assert "global_tool" in registry._tools
        assert "local_tool" not in registry._tools  # isolation

    def test_copy_mcp_isolation(self):
        registry = AgentToolRegistry()
        mcp = SlackMCPServer("xoxb-token")
        registry.add(mcp)

        copied = registry.copy()
        copied.add(SlackMCPServer("xoxb-other"))

        assert len(registry._mcp_servers) == 1
        assert len(copied._mcp_servers) == 2

    def test_schema_with_mcp(self):
        registry = AgentToolRegistry()
        registry.add(
            "local_tool",
            lambda: "result",
            description="A local tool",
            parameters={},
            required=[],
        )
        registry.add(SlackMCPServer("xoxb-token"))

        openai_schemas = registry.schema("openai")
        assert len(openai_schemas) == 2
        assert openai_schemas[0]["type"] == "function"
        assert openai_schemas[1]["type"] == "mcp"

        anthropic_schemas = registry.schema("anthropic")
        assert len(anthropic_schemas) == 2
        assert "name" in anthropic_schemas[0]
        assert anthropic_schemas[1]["type"] == "mcp"


class TestSlackMCPServer:
    """Unit tests for SlackMCPServer schema generation."""

    def test_openai_schema(self):
        mcp = SlackMCPServer("xoxb-test-token")
        schema = mcp.to_openai_schema()
        assert schema["type"] == "mcp"
        assert schema["server_label"] == "slack"
        assert schema["server_url"] == "https://mcp.slack.com/mcp"
        assert schema["headers"] == {"Authorization": "Bearer xoxb-test-token"}
        assert schema["require_approval"] == "never"

    def test_anthropic_schema(self):
        mcp = SlackMCPServer("xoxb-test-token")
        schema = mcp.to_anthropic_schema()
        assert schema["type"] == "mcp"
        assert schema["server_name"] == "slack"
        assert schema["server_url"] == "https://mcp.slack.com/mcp"
        assert schema["authorization_token"] == "xoxb-test-token"

    def test_custom_server_url(self):
        mcp = SlackMCPServer(
            "xoxb-token",
            server_url="https://mcp.dev.slack.com/mcp",
            server_label="slack-dev",
            require_approval="always",
        )
        schema = mcp.to_openai_schema()
        assert schema["server_url"] == "https://mcp.dev.slack.com/mcp"
        assert schema["server_label"] == "slack-dev"
        assert schema["require_approval"] == "always"


class TestAppAgentIntegration:
    """Integration tests for agent injection via app.py."""

    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    web_client = WebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def test_agent_available_in_event_handler(self):
        app = App(client=self.web_client)
        state = {"agent_received": False}

        @app.event("app_mention")
        def handle_app_mention(agent, body):
            assert agent is not None
            assert isinstance(agent, AgentUtilities)
            state["agent_received"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

        count = 0
        while not state["agent_received"] and count < 20:
            sleep(0.1)
            count += 1
        assert state["agent_received"] is True

    def test_agent_tools_schema_returns_registered_tools(self):
        app = App(client=self.web_client)

        @app.agent.tool("search_docs")
        def search_docs(query: str) -> str:
            """Search company documentation."""
            return f"results for {query}"

        state = {"schemas_checked": False}

        @app.event("app_mention")
        def handle_app_mention(agent):
            schemas = agent.tools.schema("openai")
            assert len(schemas) >= 1
            names = [s["function"]["name"] for s in schemas if s.get("type") == "function"]
            assert "search_docs" in names
            state["schemas_checked"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

        count = 0
        while not state["schemas_checked"] and count < 20:
            sleep(0.1)
            count += 1
        assert state["schemas_checked"] is True

    def test_agent_tools_add_does_not_affect_global(self):
        app = App(client=self.web_client)

        @app.agent.tool("global_tool")
        def global_tool() -> str:
            """A global tool."""
            return "global"

        state = {"checked": False}

        @app.event("app_mention")
        def handle_app_mention(agent):
            # Add a local tool
            agent.tools.add(
                "local_tool",
                lambda: "local",
                description="A local tool",
                parameters={},
                required=[],
            )
            local_schemas = agent.tools.schema("openai")
            local_names = [s["function"]["name"] for s in local_schemas if s.get("type") == "function"]
            assert "global_tool" in local_names
            assert "local_tool" in local_names

            # Global should not have local_tool
            global_schemas = app.agent.tools.schema("openai")
            global_names = [s["function"]["name"] for s in global_schemas if s.get("type") == "function"]
            assert "global_tool" in global_names
            assert "local_tool" not in global_names

            state["checked"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

        count = 0
        while not state["checked"] and count < 20:
            sleep(0.1)
            count += 1
        assert state["checked"] is True

    def test_app_agent_tool_decorator(self):
        app = App(client=self.web_client)

        @app.agent.tool("my_tool")
        def my_tool(arg: str) -> str:
            """Does something."""
            return arg

        schemas = app.agent.tools.schema("openai")
        assert len(schemas) == 1
        assert schemas[0]["function"]["name"] == "my_tool"
        assert schemas[0]["function"]["description"] == "Does something."

    def test_app_agent_tool_mcp_registration(self):
        app = App(client=self.web_client)
        app.agent.tool(SlackMCPServer("xoxb-token"))

        schemas = app.agent.tools.schema("openai")
        assert len(schemas) == 1
        assert schemas[0]["type"] == "mcp"

    def test_agent_property_returns_same_instance(self):
        app = App(client=self.web_client)
        assert app.agent is app.agent

    def test_agent_context_has_correct_values(self):
        app = App(client=self.web_client)
        state = {"checked": False}

        @app.event("app_mention")
        def handle_app_mention(agent, context):
            assert agent.channel_id == context.channel_id
            assert agent.thread_ts == context.thread_ts
            assert agent.team_id == context.team_id
            state["checked"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

        count = 0
        while not state["checked"] and count < 20:
            sleep(0.1)
            count += 1
        assert state["checked"] is True


# ---- Test fixtures ----


def build_payload(event: dict) -> dict:
    return {
        "token": "verification_token",
        "team_id": "T111",
        "enterprise_id": "E111",
        "api_app_id": "A111",
        "event": event,
        "type": "event_callback",
        "event_id": "Ev111",
        "event_time": 1599616881,
        "authorizations": [
            {
                "enterprise_id": "E111",
                "team_id": "T111",
                "user_id": "W111",
                "is_bot": True,
                "is_enterprise_install": False,
            }
        ],
    }


app_mention_event_body = build_payload(
    {
        "type": "app_mention",
        "user": "W222",
        "text": "<@W111> hello",
        "ts": "1726133700.887259",
        "channel": "C111",
        "event_ts": "1726133700.887259",
        "thread_ts": "1726133698.626339",
    }
)
