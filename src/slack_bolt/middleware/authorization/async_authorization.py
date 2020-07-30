from ..async_middleware import AsyncMiddleware
from ... import BoltResponse
from ...request.async_request import AsyncBoltRequest


class AsyncAuthorization(AsyncMiddleware):

    def _is_url_verification(self, req: AsyncBoltRequest) -> bool:
        return req \
               and req.payload \
               and req.payload.get("type", None) == "url_verification"

    def _is_ssl_check(self, req: AsyncBoltRequest) -> bool:
        return req \
               and req.payload \
               and req.payload.get("type", None) == "ssl_check"

    def is_no_auth_required(self, req: BoltResponse) -> bool:
        return self._is_url_verification(req) or self._is_ssl_check(req)

    @staticmethod
    def build_error_response() -> BoltResponse:
        # show an ephemeral message to the end-user
        return BoltResponse(status=200, body=":x: Please install this app into the workspace :bow:")
