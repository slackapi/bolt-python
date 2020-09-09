import copy
import sys
from typing import Optional, Union, Dict, List, Any

from slack_sdk import WebClient
from slack_sdk.models import JsonObject

from slack_bolt.error import BoltError
from slack_bolt.version import __version__ as bolt_version


def create_web_client(token: Optional[str] = None) -> WebClient:
    return WebClient(token=token, user_agent_prefix=f"Bolt/{bolt_version}",)


def convert_to_dict_list(objects: List[Union[Dict, JsonObject]]) -> List[Dict]:
    return [convert_to_dict(elm) for elm in objects]


def convert_to_dict(obj: Union[Dict, JsonObject]) -> Dict:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, JsonObject) or hasattr(obj, "to_dict"):
        return obj.to_dict()
    raise BoltError(f"{obj} (type: {type(obj)}) is unsupported")


def create_copy(original: Any) -> Any:
    if sys.version_info.major == 3 and sys.version_info.minor <= 6:
        # NOTE: Unfortunately, copy.deepcopy doesn't work in Python 3.6.5.
        # --------------------
        # >     rv = reductor(4)
        # E     TypeError: can't pickle _thread.RLock objects
        # ../../.pyenv/versions/3.6.10/lib/python3.6/copy.py:169: TypeError
        # --------------------
        # As a workaround, this operation uses shallow copies in Python 3.6.
        # If your code modifies the shared data in threads / async functions, race conditions may arise.
        # Please consider upgrading Python major version to 3.7+ if you encounter some issues due to this.
        return copy.copy(original)
    else:
        return copy.deepcopy(original)
