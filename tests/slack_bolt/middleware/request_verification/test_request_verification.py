from time import time

import pytest
from slack_sdk.signature import SignatureVerifier

from slack_bolt.middleware import RequestVerification
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


def next():
    return BoltResponse(status=200, body="next")


class TestRequestVerification:
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

    def test_valid(self):
        middleware = RequestVerification(signing_secret=self.signing_secret)
        timestamp = str(int(time()))
        raw_body = "payload={}"
        req = BoltRequest(body=raw_body, headers=self.build_headers(timestamp, raw_body))
        resp = BoltResponse(status=404, body="default")
        resp = middleware.process(req=req, resp=resp, next=next)
        assert resp.status == 200
        assert resp.body == "next"

    def test_invalid(self):
        middleware = RequestVerification(signing_secret=self.signing_secret)
        req = BoltRequest(body="payload={}", headers={})
        resp = BoltResponse(status=404)
        resp = middleware.process(req=req, resp=resp, next=next)
        assert resp.status == 401
        assert resp.body == """{"error": "invalid request"}"""

    def test_ssl_check_param_requires_valid_signature(self):
        middleware = RequestVerification(signing_secret=self.signing_secret)
        req = BoltRequest(
            body="token=random&ssl_check=1",
            headers={
                "content-type": ["application/x-www-form-urlencoded"],
                "x-slack-signature": ["v0=invalid"],
                "x-slack-request-timestamp": ["0"],
            },
        )
        resp = BoltResponse(status=404)
        resp = middleware.process(req=req, resp=resp, next=next)
        assert resp.status == 401
        assert resp.body == """{"error": "invalid request"}"""

    def test_empty_signing_secret_does_not_raise_on_init(self):
        RequestVerification(signing_secret="")

    def test_socket_mode_request_skips_verification_without_signing_secret(self):
        middleware = RequestVerification(signing_secret="")
        req = BoltRequest(mode="socket_mode", body="payload={}", headers={})
        resp = BoltResponse(status=404, body="default")
        resp = middleware.process(req=req, resp=resp, next=next)
        assert resp.status == 200
        assert resp.body == "next"

    def test_http_request_with_empty_signing_secret_raises(self):
        middleware = RequestVerification(signing_secret="")
        req = BoltRequest(body="payload={}", headers={})
        resp = BoltResponse(status=404)
        with pytest.raises(ValueError):
            middleware.process(req=req, resp=resp, next=next)
