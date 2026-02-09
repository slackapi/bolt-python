import logging
from typing import Callable, Dict, List, Optional, Union

from slack_bolt.context.agent.mcp import SlackMCPServer
from slack_bolt.context.agent.tool_registry import AgentToolRegistry


class AsyncAppAgent:
    """Experimental: App-level agent for async apps, returned by ``app.agent``.

    Holds the global tool registry and provides the ``@app.agent.tool()`` decorator
    for registering tools at app startup time. Tool registration itself is synchronous
    since it happens during app initialization.

    Attributes:
        tools: The global tool registry shared across all requests.
    """

    def __init__(self, *, logger: Optional[logging.Logger] = None):
        self._logger = logger or logging.getLogger(__name__)
        self.tools = AgentToolRegistry()

    def tool(
        self,
        name_or_mcp: Union[str, SlackMCPServer],
        *,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, dict]] = None,
        required: Optional[List[str]] = None,
        title: Optional[str] = None,
    ) -> Union[Callable, None]:
        """Register a tool or MCP server with the global registry.

        When called with a string name, returns a decorator that registers the
        decorated function as a tool::

            @app.agent.tool("search_docs")
            async def search_docs(query: str) -> str:
                \"\"\"Search company documentation.\"\"\"
                return results

        When called with a ``SlackMCPServer``, registers it directly::

            app.agent.tool(SlackMCPServer(os.environ["SLACK_BOT_TOKEN"]))

        Args:
            name_or_mcp: Tool name (str) or a ``SlackMCPServer`` instance.
            description: Tool description. Falls back to the handler's docstring.
            parameters: JSON Schema properties dict. Falls back to type introspection.
            required: List of required parameter names. Falls back to introspection.
            title: Optional display title for Slack UI during execution.

        Returns:
            A decorator when called with a string name, or ``None`` when called
            with a ``SlackMCPServer``.
        """
        if isinstance(name_or_mcp, SlackMCPServer):
            self.tools.add(name_or_mcp)
            return None

        name = name_or_mcp

        def decorator(func: Callable) -> Callable:
            self.tools.register(
                name,
                func,
                description=description,
                parameters=parameters,
                required=required,
                title=title,
            )
            return func

        return decorator
