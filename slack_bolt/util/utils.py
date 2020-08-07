from typing import Optional, Union, Dict, List

from slack_sdk import WebClient
from slack_sdk.models import JsonObject

from slack_bolt.error import BoltError
from slack_bolt.version import __version__ as bolt_version


def create_web_client(token: Optional[str] = None) -> WebClient:
    return WebClient(token=token, user_agent_prefix=f"Bolt/{bolt_version}",)


def convert_to_dict_list(objects: List[Union[Dict, JsonObject]]) -> List[Dict]:
    return [_to_dict(elm) for elm in objects]


def _to_dict(obj: Union[Dict, JsonObject]) -> Dict:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, JsonObject) or hasattr(obj, "to_dict"):
        return obj.to_dict()
    raise BoltError(f"{obj} (type: {type(obj)}) is unsupported")
