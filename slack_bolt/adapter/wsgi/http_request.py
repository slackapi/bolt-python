from typing import Any, Dict

from .utils import ENCODING


class WsgiHttpRequest:
    __slots__ = ("query_string", "environ")

    def __init__(self, environ: Dict[str, Any]):
        self.query_string = environ.get("QUERY_STRING", "")
        self.environ = environ

    def get_headers(self) -> Dict[str, str]:
        headers = {}
        for key, value in self.environ.items():
            if key in {"CONTENT_LENGTH", "CONTENT_TYPE"}:
                name = key.lower().replace("_", "-")
                headers[name] = value
            if key.startswith("HTTP_"):
                name = key[len("HTTP_") :].lower().replace("_", "-")
                headers[name] = value
        return headers

    def get_raw_body(self) -> str:
        if "wsgi.input" not in self.environ:
            return ""
        content_length = int(self.environ.get("CONTENT_LENGTH", 0))
        return self.environ["wsgi.input"].read(content_length).decode(ENCODING)
