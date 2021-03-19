import logging
import signal
import sys
from threading import Event

from slack_sdk.socket_mode.client import BaseSocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt import App
from slack_bolt.util.utils import get_boot_message


class BaseSocketModeHandler:
    app: App  # type: ignore
    client: BaseSocketModeClient

    def handle(self, client: BaseSocketModeClient, req: SocketModeRequest) -> None:
        raise NotImplementedError()

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def close(self):
        self.client.close()

    def start(self):
        self.connect()
        if self.app.logger.level > logging.INFO:
            print(get_boot_message())
        else:
            self.app.logger.info(get_boot_message())

        if sys.platform == "win32":
            # Ctrl+C etc does not work on Windows OS
            # see https://bugs.python.org/issue35935 for details
            signal.signal(signal.SIGINT, signal.SIG_DFL)

        Event().wait()
