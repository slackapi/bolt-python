from slack_bolt.middleware.request_parsing.async_request_parsing import AsyncRequestParsing
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


async def async_parse_request(req: AsyncBoltRequest) -> AsyncBoltRequest:
    async def next_():
        return BoltResponse(status=200)

    await AsyncRequestParsing().async_process(req=req, resp=BoltResponse(status=200), next=next_)
    return req
