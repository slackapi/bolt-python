import asyncio
import inspect
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from slack_bolt.context.agent.mcp import SlackMCPServer

logger = logging.getLogger(__name__)


# Mapping of Python types to JSON Schema types
_TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _introspect_parameters(func: Callable) -> Tuple[Dict[str, dict], List[str]]:
    """Inspect a function's type annotations and docstring to build JSON Schema properties.

    Args:
        func: The function to introspect.

    Returns:
        A tuple of (properties dict, required parameter names list).
    """
    sig = inspect.signature(func)
    hints = {}
    try:
        hints = {k: v for k, v in func.__annotations__.items() if k != "return"}
    except AttributeError:
        pass

    properties: Dict[str, dict] = {}
    required: List[str] = []

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue

        prop: dict = {}

        # Determine type from annotation
        annotation = hints.get(param_name)
        if annotation is not None:
            json_type = _TYPE_MAP.get(annotation)
            if json_type:
                prop["type"] = json_type
            else:
                prop["type"] = "string"
        else:
            prop["type"] = "string"

        properties[param_name] = prop

        # Parameters without defaults are required
        if param.default is inspect.Parameter.empty:
            required.append(param_name)

    return properties, required


class ToolDefinition:
    """Experimental: Internal representation of a registered tool.

    Attributes:
        name: Tool name used for dispatch.
        description: Human-readable description of what the tool does.
        parameters: JSON Schema ``properties`` dict describing the tool's parameters.
        required: List of required parameter names.
        handler: The callable that implements the tool.
        title: Optional display title shown in Slack UI during execution.
    """

    def __init__(
        self,
        *,
        name: str,
        description: str,
        parameters: Dict[str, dict],
        required: List[str],
        handler: Callable,
        title: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.required = required
        self.handler = handler
        self.title = title

    def to_openai_schema(self) -> dict:
        """Generate OpenAI function tool schema.

        Returns:
            Dict in OpenAI's function tool format::

                {
                    "type": "function",
                    "function": {
                        "name": "...",
                        "description": "...",
                        "parameters": {"type": "object", "properties": {...}, "required": [...]}
                    }
                }
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": self.required,
                },
            },
        }

    def to_anthropic_schema(self) -> dict:
        """Generate Anthropic tool schema.

        Returns:
            Dict in Anthropic's tool format::

                {
                    "name": "...",
                    "description": "...",
                    "input_schema": {"type": "object", "properties": {...}, "required": [...]}
                }
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": self.parameters,
                "required": self.required,
            },
        }


class AgentToolRegistry:
    """Experimental: Registry holding tool definitions and MCP server configurations.

    Provides methods to register tools, generate provider-specific schemas, and
    dispatch tool calls. A global instance lives on ``AppAgent`` and is copied
    per-request into ``AgentUtilities`` for isolation.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}
        self._mcp_servers: List[SlackMCPServer] = []

    def _register(
        self,
        name: str,
        handler: Callable,
        *,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, dict]] = None,
        required: Optional[List[str]] = None,
        title: Optional[str] = None,
    ) -> ToolDefinition:
        """Internal: register a tool by name and handler.

        If ``parameters`` and ``required`` are not provided, they are introspected
        from the handler's type annotations. If ``description`` is not provided,
        it is extracted from the handler's docstring.

        Args:
            name: Unique tool name for dispatch.
            handler: Callable implementing the tool logic.
            description: Human-readable description. Falls back to the handler's docstring.
            parameters: JSON Schema properties dict. Falls back to type annotation introspection.
            required: List of required parameter names. Falls back to introspection.
            title: Optional display title for Slack UI during execution.

        Returns:
            The registered ``ToolDefinition``.
        """
        if description is None:
            description = inspect.getdoc(handler) or ""

        if parameters is None or required is None:
            introspected_params, introspected_required = _introspect_parameters(handler)
            if parameters is None:
                parameters = introspected_params
            if required is None:
                required = introspected_required

        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            required=required,
            handler=handler,
            title=title,
        )
        self._tools[name] = tool_def
        return tool_def

    def add(
        self,
        name_or_obj: Union[str, ToolDefinition, SlackMCPServer],
        handler: Optional[Callable] = None,
        *,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, dict]] = None,
        required: Optional[List[str]] = None,
        title: Optional[str] = None,
    ) -> Optional[ToolDefinition]:
        """Unified public API for adding tools and MCP servers to the registry.

        Supports three call signatures:

        1. **Register a tool by name and handler**::

               registry.add("search", search_handler, description="Search docs")

        2. **Add a pre-built ToolDefinition**::

               registry.add(ToolDefinition(...))

        3. **Add an MCP server**::

               registry.add(SlackMCPServer("xoxb-token"))

        Args:
            name_or_obj: A tool name (str), ``ToolDefinition``, or ``SlackMCPServer``.
            handler: Callable implementing the tool (only when ``name_or_obj`` is a str).
            description: Human-readable description. Falls back to the handler's docstring.
            parameters: JSON Schema properties dict. Falls back to type introspection.
            required: List of required parameter names. Falls back to introspection.
            title: Optional display title for Slack UI during execution.

        Returns:
            The registered ``ToolDefinition`` when adding a tool, or ``None`` for MCP servers.

        Raises:
            TypeError: If arguments are invalid (e.g., handler with MCP server,
                missing handler with string name).
        """
        if isinstance(name_or_obj, str):
            if handler is None:
                raise TypeError("handler is required when adding a tool by name")
            return self._register(
                name_or_obj,
                handler,
                description=description,
                parameters=parameters,
                required=required,
                title=title,
            )
        elif isinstance(name_or_obj, SlackMCPServer):
            if handler is not None:
                raise TypeError("handler cannot be provided when adding a SlackMCPServer")
            self._mcp_servers.append(name_or_obj)
            return None
        elif isinstance(name_or_obj, ToolDefinition):
            if handler is not None:
                raise TypeError("handler cannot be provided when adding a ToolDefinition")
            self._tools[name_or_obj.name] = name_or_obj
            return name_or_obj
        else:
            raise TypeError(
                f"Expected str, ToolDefinition, or SlackMCPServer, got {type(name_or_obj)}"
            )

    def schema(self, provider: str) -> List[dict]:
        """Generate provider-specific tool schemas for all registered tools and MCP servers.

        Args:
            provider: LLM provider name — ``"openai"`` or ``"anthropic"``.

        Returns:
            List of tool schema dicts in the provider's expected format.

        Raises:
            ValueError: If the provider is not supported.
        """
        if provider == "openai":
            schemas: List[dict] = [t.to_openai_schema() for t in self._tools.values()]
            schemas.extend(m.to_openai_schema() for m in self._mcp_servers)
            return schemas
        elif provider == "anthropic":
            schemas = [t.to_anthropic_schema() for t in self._tools.values()]
            schemas.extend(m.to_anthropic_schema() for m in self._mcp_servers)
            return schemas
        else:
            raise ValueError(f"Unsupported provider: {provider!r}. Use 'openai' or 'anthropic'.")

    def execute(self, streamer: Any, call_id: str, name: str, arguments: dict) -> Any:
        """Synchronously dispatch a tool call by name.

        Sends a ``TaskUpdateChunk`` status update via the streamer before and after
        execution, then invokes the registered handler with the provided arguments.

        Args:
            streamer: Chat stream instance for sending UI status updates.
            call_id: Tool call ID from the LLM response (used as task ID in the UI).
            name: Tool name to look up in the registry.
            arguments: Dict of arguments to pass to the tool handler.

        Returns:
            The tool handler's return value.

        Raises:
            KeyError: If the tool name is not registered.
        """
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name!r}")

        tool = self._tools[name]
        title = tool.title or tool.name

        # Send "in_progress" status
        try:
            streamer.append(
                task_update={"id": call_id, "title": title, "status": "in_progress"}
            )
        except Exception:
            logger.debug(f"Failed to send in_progress status for tool {name!r}", exc_info=True)

        try:
            result = tool.handler(**arguments)

            # Send "completed" status
            try:
                streamer.append(
                    task_update={"id": call_id, "title": title, "status": "completed"}
                )
            except Exception:
                logger.debug(f"Failed to send completed status for tool {name!r}", exc_info=True)

            return result

        except Exception as e:
            # Send "failed" status
            try:
                streamer.append(
                    task_update={"id": call_id, "title": title, "status": "failed"}
                )
            except Exception:
                logger.debug(f"Failed to send failed status for tool {name!r}", exc_info=True)
            raise

    async def async_execute(self, streamer: Any, call_id: str, name: str, arguments: dict) -> Any:
        """Asynchronously dispatch a tool call by name.

        Same as :meth:`execute` but awaits coroutine handlers.

        Args:
            streamer: Chat stream instance for sending UI status updates.
            call_id: Tool call ID from the LLM response (used as task ID in the UI).
            name: Tool name to look up in the registry.
            arguments: Dict of arguments to pass to the tool handler.

        Returns:
            The tool handler's return value.

        Raises:
            KeyError: If the tool name is not registered.
        """
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name!r}")

        tool = self._tools[name]
        title = tool.title or tool.name

        # Send "in_progress" status
        try:
            streamer.append(
                task_update={"id": call_id, "title": title, "status": "in_progress"}
            )
        except Exception:
            logger.debug(f"Failed to send in_progress status for tool {name!r}", exc_info=True)

        try:
            result = tool.handler(**arguments)
            if asyncio.iscoroutine(result):
                result = await result

            # Send "completed" status
            try:
                streamer.append(
                    task_update={"id": call_id, "title": title, "status": "completed"}
                )
            except Exception:
                logger.debug(f"Failed to send completed status for tool {name!r}", exc_info=True)

            return result

        except Exception as e:
            # Send "failed" status
            try:
                streamer.append(
                    task_update={"id": call_id, "title": title, "status": "failed"}
                )
            except Exception:
                logger.debug(f"Failed to send failed status for tool {name!r}", exc_info=True)
            raise

    def copy(self) -> "AgentToolRegistry":
        """Create a shallow copy of this registry for per-request isolation.

        The copy shares the same ``ToolDefinition`` and ``SlackMCPServer`` objects,
        but adding new tools/MCP servers to the copy won't affect the original.

        Returns:
            A new ``AgentToolRegistry`` with the same tools and MCP servers.
        """
        new_registry = AgentToolRegistry()
        new_registry._tools = dict(self._tools)
        new_registry._mcp_servers = list(self._mcp_servers)
        return new_registry
