import asyncio
import logging
import threading
import time
from unittest import TestCase
from urllib.error import URLError
from urllib.request import urlopen

from aiohttp import WSMsgType, web

socket_mode_envelopes = [
    """{"envelope_id":"57d6a792-4d35-4d0b-b6aa-3361493e1caf","payload":{"type":"shortcut","token":"xxx","action_ts":"1610198080.300836","team":{"id":"T111","domain":"seratch"},"user":{"id":"U111","username":"seratch","team_id":"T111"},"is_enterprise_install":false,"enterprise":null,"callback_id":"do-something","trigger_id":"111.222.xxx"},"type":"interactive","accepts_response_payload":false}""",
    """{"envelope_id":"1d3c79ab-0ffb-41f3-a080-d19e85f53649","payload":{"token":"xxx","team_id":"T111","team_domain":"xxx","channel_id":"C111","channel_name":"random","user_id":"U111","user_name":"seratch","command":"/hello-socket-mode","text":"","api_app_id":"A111","response_url":"https://hooks.slack.com/commands/T111/111/xxx","trigger_id":"111.222.xxx"},"type":"slash_commands","accepts_response_payload":true}""",
    """{"envelope_id":"08cfc559-d933-402e-a5c1-79e135afaae4","payload":{"token":"xxx","team_id":"T111","api_app_id":"A111","event":{"client_msg_id":"c9b466b5-845c-49c6-a371-57ae44359bf1","type":"message","text":"<@W111>","user":"U111","ts":"1610197986.000300","team":"T111","blocks":[{"type":"rich_text","block_id":"1HBPc","elements":[{"type":"rich_text_section","elements":[{"type":"user","user_id":"U111"}]}]}],"channel":"C111","event_ts":"1610197986.000300","channel_type":"channel"},"type":"event_callback","event_id":"Ev111","event_time":1610197986,"authorizations":[{"enterprise_id":null,"team_id":"T111","user_id":"U111","is_bot":true,"is_enterprise_install":false}],"is_ext_shared_channel":false,"event_context":"1-message-T111-C111"},"type":"events_api","accepts_response_payload":false,"retry_attempt":1,"retry_reason":"timeout"}""",
]


def start_thread_socket_mode_server(test: TestCase, port: int):
    logger = logging.getLogger(__name__)
    state = {}

    def reset_server_state():
        state.update(
            envelopes_to_consume=list(socket_mode_envelopes),
        )

    test.reset_server_state = reset_server_state

    async def health(request: web.Request):
        wr = web.Response()
        await wr.prepare(request)
        wr.set_status(200)
        return wr

    async def link(request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type != WSMsgType.TEXT:
                continue

            if state["envelopes_to_consume"]:
                e = state["envelopes_to_consume"].pop(0)
                logger.debug(f"Send an envelope: {e}")
                await ws.send_str(e)

            message = msg.data
            logger.debug(f"Server received a message: {message}")

            await ws.send_str(message)

        return ws

    app = web.Application()
    app.add_routes(
        [
            web.get("/link", link),
            web.get("/health", health),
        ]
    )
    runner = web.AppRunner(app)

    def run_server():
        reset_server_state()

        test.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(test.loop)
        test.loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, "127.0.0.1", port, reuse_port=True)
        test.loop.run_until_complete(site.start())

        # run until it's stopped from the main thread
        test.loop.run_forever()

        test.loop.run_until_complete(runner.cleanup())
        test.loop.close()

    return run_server


def start_socket_mode_server(test, port: int):
    test.sm_thread = threading.Thread(target=start_thread_socket_mode_server(test, port))
    test.sm_thread.daemon = True
    test.sm_thread.start()
    wait_for_socket_mode_server(port, 4)


def wait_for_socket_mode_server(port: int, timeout: int):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        try:
            urlopen(f"http://127.0.0.1:{port}/health")
            return
        except URLError:
            time.sleep(0.01)


def stop_socket_mode_server(test: TestCase):
    # An event loop runs in a thread and executes all callbacks and Tasks in
    # its thread. While a Task is running in the event loop, no other Tasks
    # can run in the same thread. When a Task executes an await expression, the
    # running Task gets suspended, and the event loop executes the next Task.
    # To schedule a callback from another OS thread, the loop.call_soon_threadsafe() method should be used.
    # https://docs.python.org/3/library/asyncio-dev.html#asyncio-multithreading
    test.loop.call_soon_threadsafe(test.loop.stop)
    test.sm_thread.join(timeout=5)
