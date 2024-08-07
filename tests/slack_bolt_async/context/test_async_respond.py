import pytest

from tests.utils import get_event_loop
from slack_bolt.context.respond.async_respond import AsyncRespond
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    setup_mock_web_api_server_async,
)


class TestAsyncRespond:
    @pytest.fixture
    def event_loop(self):
        setup_mock_web_api_server_async(self)
        loop = get_event_loop()
        yield loop
        loop.close()
        cleanup_mock_web_api_server_async(self)

    @pytest.mark.asyncio
    async def test_respond(self):
        response_url = "http://localhost:8888"
        respond = AsyncRespond(response_url=response_url)
        response = await respond(text="Hi there!")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_respond2(self):
        response_url = "http://localhost:8888"
        respond = AsyncRespond(response_url=response_url)
        response = await respond({"text": "Hi there!"})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_respond_unfurl_options(self):
        response_url = "http://localhost:8888"
        respond = AsyncRespond(response_url=response_url)
        response = await respond(text="Hi there!", unfurl_media=True, unfurl_links=True)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_metadata(self):
        response_url = "http://localhost:8888"
        respond = AsyncRespond(response_url=response_url)
        response = await respond(
            text="Hi there!",
            response_type="in_channel",
            metadata={"event_type": "foo", "event_payload": {"foo": "bar"}},
        )
        assert response.status_code == 200
