import json
import asyncio
from time import time
from typing import Callable, Awaitable, Optional

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt import BoltResponse
from slack_bolt.listener.async_listener import AsyncCustomListener
from slack_bolt.listener.asyncio_runner import AsyncioListenerRunner
from slack_bolt.listener_matcher.async_listener_matcher import AsyncCustomListenerMatcher
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.request.payload_utils import is_shortcut
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    assert_auth_test_count_async,
    setup_mock_web_api_server_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


# Note that async middleware system does not support instance methods n a class.
class TestAsyncMiddleware:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server_async(self)
        try:
            yield  # run the test here
        finally:
            cleanup_mock_web_api_server_async(self)
            restore_os_env(old_os_env)

    def build_request(self) -> AsyncBoltRequest:
        body = {
            "type": "shortcut",
            "token": "verification_token",
            "action_ts": "111.111",
            "team": {
                "id": "T111",
                "domain": "workspace-domain",
                "enterprise_id": "E111",
                "enterprise_name": "Org Name",
            },
            "user": {"id": "W111", "username": "primary-owner", "team_id": "T111"},
            "callback_id": "test-shortcut",
            "trigger_id": "111.111.xxxxxx",
        }
        timestamp, body = str(int(time())), json.dumps(body)
        return AsyncBoltRequest(
            body=body,
            headers={
                "content-type": ["application/json"],
                "x-slack-signature": [
                    self.signature_verifier.generate_signature(
                        body=body,
                        timestamp=timestamp,
                    )
                ],
                "x-slack-request-timestamp": [timestamp],
            },
        )

    @pytest.mark.asyncio
    async def test_no_next_call(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(no_next)
        app.shortcut("test-shortcut")(just_ack)

        response = await app.async_dispatch(self.build_request())
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_next_call(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(just_next)
        app.shortcut("test-shortcut")(just_ack)

        response = await app.async_dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_decorator_next_call(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        @app.middleware
        async def just_next(next):
            await next()

        app.shortcut("test-shortcut")(just_ack)

        response = await app.async_dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_next_underscore_call(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(just_next_)
        app.shortcut("test-shortcut")(just_ack)

        response = await app.async_dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_decorator_next_underscore_call(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        @app.middleware
        async def just_next_(next_):
            await next_()

        app.shortcut("test-shortcut")(just_ack)

        response = await app.async_dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_lazy_listener_middleware(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        unmatch_middleware = LazyListenerStarter("xxxx")
        app.use(unmatch_middleware)

        response = await app.async_dispatch(self.build_request())
        assert response.status == 404

        my_middleware = LazyListenerStarter("test-shortcut")
        app.use(my_middleware)
        response = await app.async_dispatch(self.build_request())
        assert response.status == 200
        count = 0
        while count < 20 and my_middleware.lazy_called is False:
            await asyncio.sleep(0.05)
        assert my_middleware.lazy_called is True


async def just_ack(ack):
    await ack("acknowledged!")


async def no_next():
    pass


async def just_next(next):
    await next()


async def just_next_(next_):
    await next_()


class LazyListenerStarter(AsyncMiddleware):
    lazy_called: bool
    callback_id: str

    def __init__(self, callback_id: str):
        self.lazy_called = False
        self.callback_id = callback_id

    async def lazy_listener(self):
        self.lazy_called = True

    async def async_process(
        self, *, req: AsyncBoltRequest, resp: BoltResponse, next: Callable[[], Awaitable[BoltResponse]]
    ) -> Optional[BoltResponse]:
        async def is_target(payload: dict):
            return payload.get("callback_id") == self.callback_id

        if is_shortcut(req.body):
            listener = AsyncCustomListener(
                app_name="test-app",
                ack_function=just_ack,
                lazy_functions=[self.lazy_listener],
                matchers=[
                    AsyncCustomListenerMatcher(
                        app_name="test-app",
                        func=is_target,
                    )
                ],
                middleware=[],
                base_logger=req.context.logger,
            )
            if await listener.async_matches(req=req, resp=resp):
                listener_runner: AsyncioListenerRunner = req.context.listener_runner
                response = await listener_runner.run(
                    request=req,
                    response=resp,
                    listener_name="test",
                    listener=listener,
                )
                if response is not None:
                    return response
        await next()
