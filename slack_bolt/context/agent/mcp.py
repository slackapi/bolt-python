class SlackMCPServer:
    """Experimental: Slack MCP server configuration for connecting agents to Slack capabilities.

    Wraps connection details for Slack's hosted MCP server. After registration via
    ``app.agent.tool()`` or ``agent.tools.add()``, the schema is included in
    ``agent.tools.schema()`` in the provider's expected format.

    Args:
        token: Bot or user token for authenticating with the MCP server.
        server_url: MCP server endpoint URL.
        server_label: Label for the MCP server (used in OpenAI schema).
        require_approval: Approval mode for OpenAI schema (``"never"`` or ``"always"``).
    """

    def __init__(
        self,
        token: str,
        *,
        server_url: str = "https://mcp.slack.com/mcp",
        server_label: str = "slack",
        require_approval: str = "never",
    ):
        self.token = token
        self.server_url = server_url
        self.server_label = server_label
        self.require_approval = require_approval

    def to_openai_schema(self) -> dict:
        """Generate OpenAI MCP tool schema.

        Returns:
            Dict in OpenAI's MCP tool format::

                {
                    "type": "mcp",
                    "server_label": "slack",
                    "server_url": "https://mcp.slack.com/mcp",
                    "headers": {"Authorization": "Bearer <token>"},
                    "require_approval": "never"
                }
        """
        return {
            "type": "mcp",
            "server_label": self.server_label,
            "server_url": self.server_url,
            "headers": {"Authorization": f"Bearer {self.token}"},
            "require_approval": self.require_approval,
        }

    def to_anthropic_schema(self) -> dict:
        """Generate Anthropic MCP tool schema.

        Returns:
            Dict in Anthropic's MCP tool format::

                {
                    "type": "mcp",
                    "server_name": "slack",
                    "server_url": "https://mcp.slack.com/mcp",
                    "authorization_token": "<token>"
                }
        """
        return {
            "type": "mcp",
            "server_name": self.server_label,
            "server_url": self.server_url,
            "authorization_token": self.token,
        }
