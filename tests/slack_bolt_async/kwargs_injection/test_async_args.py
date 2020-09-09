import logging

from slack_bolt import BoltResponse
from slack_bolt.kwargs_injection.async_args import AsyncArgs
from slack_bolt.kwargs_injection.async_utils import build_async_required_kwargs
from slack_bolt.request.async_request import AsyncBoltRequest


class TestAsyncArgs:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def next(self):
        pass

    def test_build(self):
        required_args = [
            "logger",
            "client",
            "req",
            "resp",
            "context",
            "body",
            "payload",
            "ack",
            "say",
            "respond",
            "next",
        ]
        arg_params: dict = build_async_required_kwargs(
            logger=logging.getLogger(__name__),
            required_arg_names=required_args,
            request=AsyncBoltRequest(body="", headers={}),
            response=BoltResponse(status=200),
            next_func=next,
        )
        args = AsyncArgs(**arg_params)
        assert args.logger is not None
        assert args.request is not None
        assert args.response is not None
        assert args.client is not None
