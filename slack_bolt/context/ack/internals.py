from typing import Optional, List, Union, Any

from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block, Option, OptionGroup

from slack_bolt.error import BoltError
from slack_bolt.response import BoltResponse
from slack_bolt.util.utils import convert_to_dict_list


def _set_response(
    self: Any,
    text_or_whole_response: Union[str, dict] = "",
    blocks: Optional[List[Union[dict, Block]]] = None,
    attachments: Optional[List[Union[dict, Attachment]]] = None,
    options: Optional[List[Union[dict, Option]]] = None,
    option_groups: Optional[List[Union[dict, OptionGroup]]] = None,
) -> BoltResponse:
    if isinstance(text_or_whole_response, str):
        text: str = text_or_whole_response
        if attachments and len(attachments) > 0:
            self.response = BoltResponse(
                status=200,
                body={"text": text, "attachments": convert_to_dict_list(attachments),},
            )
        elif blocks and len(blocks) > 0:
            self.response = BoltResponse(
                status=200, body={"text": text, "blocks": convert_to_dict_list(blocks),}
            )
        elif options and len(options) > 0:
            self.response = BoltResponse(
                status=200, body={"options": convert_to_dict_list(options),}
            )
        elif option_groups and len(option_groups) > 0:
            self.response = BoltResponse(
                status=200, body={"option_groups": convert_to_dict_list(option_groups),}
            )
        else:
            self.response = BoltResponse(status=200, body=text)
        return self.response
    elif isinstance(text_or_whole_response, dict):
        body = text_or_whole_response
        if "attachments" in body:
            body["attachments"] = convert_to_dict_list(body["attachments"])
        if "blocks" in body:
            body["blocks"] = convert_to_dict_list(body["blocks"])
        if "options" in body:
            body["options"] = convert_to_dict_list(body["options"])
        if "option_groups" in body:
            body["option_groups"] = convert_to_dict_list(body["option_groups"])

        self.response = BoltResponse(status=200, body=body)
        return self.response
    else:
        raise BoltError(
            f"{text_or_whole_response} (type: {type(text_or_whole_response)}) is unsupported"
        )
