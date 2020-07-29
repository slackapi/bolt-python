from typing import Optional, Dict


class OAuthStateCookieUtils:
    default_cookie_name = "slack-app-oauth-state"
    default_expiration_seconds = 60 * 10,  # 10 minutes

    def __init__(
        self,
        *,
        cookie_name: str = default_cookie_name,
        expiration_seconds: int = default_expiration_seconds
    ):
        self.cookie_name = cookie_name
        self.expiration_seconds = expiration_seconds

    def build_creation_header(self, state: str) -> str:
        return f"{self.cookie_name}={state}; " \
               "Secure; " \
               "HttpOnly; " \
               "Path=/; " \
               f"Max-Age={self.expiration_seconds}"

    def build_deletion_header(self) -> str:
        return f"{self.cookie_name}=deleted; " \
               "Secure; " \
               "HttpOnly; " \
               "Path=/; " \
               "Expires=Thu, 01 Jan 1970 00:00:00 GMT"

    def is_valid_browser(self, state: Optional[str], request_headers: Dict[str, str]) -> bool:
        if state is None \
            or request_headers is None \
            or request_headers.get("cookie", None) is None:
            return False
        for cookie in request_headers["cookie"]:
            if cookie == f"{self.cookie_name}={state}":
                return True
        return False
