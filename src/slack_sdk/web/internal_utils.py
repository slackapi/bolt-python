import json
import platform
import sys
from typing import Dict
from typing import Union, List

import slack.version as slack_version

from slack_sdk.errors import SlackRequestError
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.block_kit import Block


def convert_bool_to_0_or_1(params: Dict[str, any]) -> Dict[str, any]:
    """Converts all bool values in dict to "0" or "1".

    Slack APIs safely accept "0"/"1" as boolean values.
    Using True/False (bool in Python) doesn't work with aiohttp.
    This method converts only the bool values in top-level of a given dict.

    :param params: params as a dict
    :return: return modified dict
    """
    if params:
        return {k: _to_0_or_1_if_bool(v) for k, v in params.items()}
    return None


def get_user_agent():
    """Construct the user-agent header with the package info,
    Python version and OS version.

    Returns:
        The user agent string.
        e.g. 'Python/3.6.7 slackclient/2.0.0 Darwin/17.7.0'
    """
    # __name__ returns all classes, we only want the client
    client = "{0}/{1}".format("slackclient", slack_version.__version__)
    python_version = "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info)
    system_info = "{0}/{1}".format(platform.system(), platform.release())
    user_agent_string = " ".join([python_version, client, system_info])
    return user_agent_string


def _parse_web_class_objects(kwargs) -> None:
    def to_dict(obj: Union[Dict, Block, Attachment]):
        if isinstance(obj, Block):
            return obj.to_dict()
        if isinstance(obj, Attachment):
            return obj.to_dict()
        return obj

    blocks = kwargs.get("blocks", None)
    if blocks is not None and isinstance(blocks, list):
        dict_blocks = [to_dict(b) for b in blocks]
        kwargs.update({"blocks": dict_blocks})

    attachments = kwargs.get("attachments", None)
    if attachments is not None and isinstance(attachments, list):
        dict_attachments = [to_dict(a) for a in attachments]
        kwargs.update({"attachments": dict_attachments})


def _update_call_participants(kwargs, users: Union[str, List[Dict[str, str]]]) -> None:
    if users is None:
        return

    if isinstance(users, list):
        kwargs.update({"users": json.dumps(users)})
    elif isinstance(users, str):
        kwargs.update({"users": users})
    else:
        raise SlackRequestError("users must be either str or List[Dict[str, str]]")


def _next_cursor_is_present(data) -> bool:
    """Determine if the response contains 'next_cursor'
    and 'next_cursor' is not empty.

    Returns:
        A boolean value.
    """
    present = (
        "response_metadata" in data
        and "next_cursor" in data["response_metadata"]
        and data["response_metadata"]["next_cursor"] != ""
    )
    return present


def _to_0_or_1_if_bool(v: any) -> str:
    if isinstance(v, bool):
        return "1" if v else "0"
    return v
