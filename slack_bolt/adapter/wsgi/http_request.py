from typing import Any, Dict, Sequence, Union

from .internals import ENCODING


class WsgiHttpRequest:
    """This Class uses the PEP 3333 standard to extract request information
    from the WSGI web server running the application

    PEP 3333: https://peps.python.org/pep-3333/
    """

    __slots__ = ("method", "path", "query_string", "protocol", "environ")

    def __init__(self, environ: Dict[str, Any]):
        self.method: str = environ.get("REQUEST_METHOD", "GET")
        self.path: str = environ.get("PATH_INFO", "")
        self.query_string: str = environ.get("QUERY_STRING", "")
        self.protocol: str = environ.get("SERVER_PROTOCOL", "")
        self.environ = environ

    def get_headers(self) -> Dict[str, Union[str, Sequence[str]]]:
        headers = {}
        for key, value in self.environ.items():
            if key in {"CONTENT_LENGTH", "CONTENT_TYPE"}:
                name = key.lower().replace("_", "-")
                headers[name] = value
            if key.startswith("HTTP_"):
                name = key[len("HTTP_"):].lower().replace("_", "-")  # fmt: skip
                headers[name] = value
        return headers

    def get_body(self) -> str:
        if "wsgi.input" not in self.environ:
            return ""
        content_length = int(self.environ.get("CONTENT_LENGTH", 0))
        return self.environ["wsgi.input"].read(content_length).decode(ENCODING)
