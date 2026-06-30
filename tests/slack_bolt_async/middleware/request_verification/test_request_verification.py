from time import time

import pytest
from slack_sdk.signature import SignatureVerifier

from slack_bolt.middleware.request_verification.async_request_verification import (
    AsyncRequestVerification,
)
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


async def next():
    return BoltResponse(status=200, body="next")


class TestAsyncRequestVerification:
    signing_secret = "secret"
    signature_verifier = SignatureVerifier(signing_secret)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    @pytest.mark.asyncio
    async def test_valid(self):
        middleware = AsyncRequestVerification(signing_secret="secret")
        timestamp = str(int(time()))
        raw_body = "payload={}"
        req = AsyncBoltRequest(body=raw_body, headers=self.build_headers(timestamp, raw_body))
        resp = BoltResponse(status=404)
        resp = await middleware.async_process(req=req, resp=resp, next=next)
        assert resp.status == 200
        assert resp.body == "next"

    @pytest.mark.asyncio
    async def test_invalid(self):
        middleware = AsyncRequestVerification(signing_secret="secret")
        req = AsyncBoltRequest(body="payload={}", headers={})
        resp = BoltResponse(status=404)
        resp = await middleware.async_process(req=req, resp=resp, next=next)
        assert resp.status == 401
        assert resp.body == """{"error": "invalid request"}"""

    @pytest.mark.asyncio
    async def test_ssl_check_param_requires_valid_signature(self):
        middleware = AsyncRequestVerification(signing_secret="secret")
        req = AsyncBoltRequest(
            body="token=random&ssl_check=1",
            headers={
                "content-type": ["application/x-www-form-urlencoded"],
                "x-slack-signature": ["v0=invalid"],
                "x-slack-request-timestamp": ["0"],
            },
        )
        resp = BoltResponse(status=404)
        resp = await middleware.async_process(req=req, resp=resp, next=next)
        assert resp.status == 401
        assert resp.body == """{"error": "invalid request"}"""

    def test_empty_signing_secret_does_not_raise_on_init(self):
        # A Socket Mode app has no signing secret. Constructing the middleware
        # must not raise, even though slack_sdk>=3.43.0 rejects an empty
        # signing secret when the SignatureVerifier is created.
        AsyncRequestVerification(signing_secret="")

    @pytest.mark.asyncio
    async def test_socket_mode_request_skips_verification_without_signing_secret(self):
        middleware = AsyncRequestVerification(signing_secret="")
        req = AsyncBoltRequest(mode="socket_mode", body="payload={}", headers={})
        resp = BoltResponse(status=404, body="default")
        resp = await middleware.async_process(req=req, resp=resp, next=next)
        assert resp.status == 200
        assert resp.body == "next"
