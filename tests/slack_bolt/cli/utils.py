import time

from typing import Optional
from slack_bolt.adapter.socket_mode.builtin import SocketModeHandler
from slack_bolt.app.app import App


def get_test_socket_mode_handler(port: int, app: App, app_token: Optional[str]) -> SocketModeHandler:
    handler = SocketModeHandler(
        app,
        app_token,
        trace_enabled=True,
    )
    handler.client.wss_uri = f"ws://localhost:{str(port)}/link"
    handler.client.default_auto_reconnect_enabled = False
    return handler


def wait_for_test_socket_connection(handler: SocketModeHandler, secs: int):
    start_time = time.time()
    while (time.time() - start_time) < secs:
        if handler.client.is_connected() is True:
            break
