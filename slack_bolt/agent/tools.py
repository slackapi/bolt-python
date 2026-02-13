import copy
import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from slack_sdk.web.chat_stream import ChatStream


@dataclass
class ToolDefinition:
    """Internal representation of a registered tool."""

    name: str
    handler: Callable[..., str]
    description: str
    parameters: Dict[str, Any]
    required: List[str]


_TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _introspect_handler(func: Callable) -> dict:
    """Extract metadata from a function signature to build JSON Schema parameters.

    Uses ``typing.get_type_hints()`` and ``inspect.signature()`` to derive
    parameter types. Falls back to the function docstring for the description.

    Returns:
        dict with keys ``description``, ``parameters``, and ``required``.
    """
    try:
        hints = __import__("typing").get_type_hints(func)
    except Exception:
        hints = {}

    sig = inspect.signature(func)
    parameters: Dict[str, Any] = {}
    required: List[str] = []

    for param_name, param in sig.parameters.items():
        json_type = _TYPE_MAP.get(hints.get(param_name), "string")
        parameters[param_name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(param_name)

    description = (func.__doc__ or "").strip()

    return {
        "description": description,
        "parameters": parameters,
        "required": required,
    }


class Tools:
    """Tool registry for AI-powered Slack agents.

    Experimental:
        This API is experimental and may change in future releases.

    Example::

        tools = Tools()

        @tools.add("search")
        def search(query: str) -> str:
            return f"Results for {query}"

        # Or programmatically:
        tools.add("greet", handler=greet_fn, description="Greet a user")
    """

    def __init__(self) -> None:
        self._definitions: Dict[str, ToolDefinition] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def add(
        self,
        name: str,
        handler: Optional[Callable[..., str]] = None,
        *,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        required: Optional[List[str]] = None,
    ):
        """Register a tool handler.

        Can be used as a decorator::

            @tools.add("search")
            def search(query: str) -> str:
                return f"Results for {query}"

        Or called programmatically::

            tools.add("search", handler=search_fn, description="Search")

        Args:
            name: Unique tool identifier.
            handler: The function to invoke. When ``None``, returns a decorator.
            description: Human-readable description. Defaults to handler docstring.
            parameters: JSON Schema properties dict. Defaults to introspected signature.
            required: Required parameter names. Defaults to introspected signature.

        Returns:
            The handler function (when used as a decorator) or ``None``.

        Raises:
            ValueError: If a tool with *name* is already registered.
        """
        if name in self._definitions:
            raise ValueError(f"Tool already registered: {name!r}")

        def _register(func: Callable[..., str]) -> Callable[..., str]:
            introspected = _introspect_handler(func)
            self._definitions[name] = ToolDefinition(
                name=name,
                handler=func,
                description=description if description is not None else introspected["description"],
                parameters=parameters if parameters is not None else introspected["parameters"],
                required=required if required is not None else introspected["required"],
            )
            return func

        if handler is not None:
            _register(handler)
            return None

        return _register

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        stream: ChatStream,
        call_id: str,
        name: str,
        arguments: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Execute a registered tool and send status updates via *stream*.

        Sends ``task_update`` kwargs through ``stream.append()`` to indicate
        ``in_progress``, ``completed``, or ``failed`` status.

        Args:
            stream: A ``ChatStream`` instance for status updates.
            call_id: Identifier for the tool call (passed in ``task_update``).
            name: The registered tool name.
            arguments: Keyword arguments forwarded to the handler.

        Returns:
            The string result from the handler.

        Raises:
            KeyError: If *name* is not registered.
        """
        if name not in self._definitions:
            raise KeyError(f"Unknown tool: {name!r}")

        definition = self._definitions[name]
        kwargs = arguments or {}

        stream.append(
            markdown_text="",
            task_update={"call_id": call_id, "status": "in_progress"},
        )

        try:
            result = definition.handler(**kwargs)
        except Exception as exc:
            stream.append(
                markdown_text="",
                task_update={"call_id": call_id, "status": "failed", "output": str(exc)},
            )
            raise

        stream.append(
            markdown_text="",
            task_update={"call_id": call_id, "status": "completed", "output": result},
        )
        return result

    # ------------------------------------------------------------------
    # Schema export
    # ------------------------------------------------------------------

    def schema(self, provider: str) -> List[Dict[str, Any]]:
        """Export tool schemas for an LLM provider.

        Args:
            provider: ``"openai"`` or ``"anthropic"``.

        Returns:
            List of tool schema dicts in the provider's format.

        Raises:
            ValueError: If *provider* is not supported.
        """
        if provider == "openai":
            return self._schema_openai()
        elif provider == "anthropic":
            return self._schema_anthropic()
        else:
            raise ValueError(f"Unsupported provider: {provider!r}. Use 'openai' or 'anthropic'.")

    def _schema_openai(self) -> List[Dict[str, Any]]:
        result = []
        for defn in self._definitions.values():
            result.append(
                {
                    "type": "function",
                    "function": {
                        "name": defn.name,
                        "description": defn.description,
                        "parameters": {
                            "type": "object",
                            "properties": defn.parameters,
                            "required": defn.required,
                        },
                    },
                }
            )
        return result

    def _schema_anthropic(self) -> List[Dict[str, Any]]:
        result = []
        for defn in self._definitions.values():
            result.append(
                {
                    "name": defn.name,
                    "description": defn.description,
                    "input_schema": {
                        "type": "object",
                        "properties": defn.parameters,
                        "required": defn.required,
                    },
                }
            )
        return result

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def copy(self) -> "Tools":
        """Create an independent copy of the registry.

        Handler references are shared; definitions are deep-copied.
        """
        new = Tools()
        for name, defn in self._definitions.items():
            new._definitions[name] = ToolDefinition(
                name=defn.name,
                handler=defn.handler,
                description=defn.description,
                parameters=copy.deepcopy(defn.parameters),
                required=list(defn.required),
            )
        return new

    def __len__(self) -> int:
        return len(self._definitions)

    def __contains__(self, name: object) -> bool:
        return name in self._definitions
