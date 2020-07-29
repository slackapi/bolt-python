from typing import List, Optional

from slack_bolt.response.response import BoltResponse


class Ack():
    def __init__(self):
        self.response: Optional[BoltResponse] = None

    def __call__(self, text: str = None, blocks: Optional[List[dict]] = None) -> BoltResponse:
        if not text and (not blocks or len(blocks) == 0):
            self.response = BoltResponse(status=200, body="")
        else:
            self.response = BoltResponse(
                status=200,
                body={
                    "text": text,
                    "blocks": blocks,
                }
            )
        return self.response
