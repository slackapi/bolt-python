import json
from typing import Union


class BoltResponse():
    def __init__(
        self,
        *,
        status: int,
        body: Union[str, dict],
        headers: dict = {},
    ):
        self.status = status
        self.body = json.dumps(body) if isinstance(body, dict) else body
        self.headers = {k.lower(): v for k, v in headers.items()}
        if "content-type" not in self.headers.keys():
            if self.body and self.body.startswith("{"):
                self.headers["content-type"] = "application/json;charset=utf-8"
            else:
                self.headers["content-type"] = "text/plain;charset=utf-8"
