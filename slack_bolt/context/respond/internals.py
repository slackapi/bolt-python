from typing import Optional, List, Dict


def _build_message(
    text: str = "",
    blocks: Optional[List[dict]] = None,
    response_type: Optional[str] = None,
    replace_original: Optional[bool] = None,
    delete_original: Optional[bool] = None,
) -> Dict[str, any]:
    message = {"text": text}
    if blocks is not None:
        message["blocks"] = blocks
    if response_type is not None:
        message["response_type"] = response_type
    if replace_original is not None:
        message["replace_original"] = replace_original
    if delete_original is not None:
        message["delete_original"] = delete_original
    return message
