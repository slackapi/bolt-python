import sys

from slack_bolt.error import BoltError

from typing import Optional, Union


if sys.version_info.major == 3 and sys.version_info.minor <= 6:
    from re import _pattern_type as Pattern
else:
    from re import Pattern


def _matches(str_or_pattern: Union[str, Pattern], input: Optional[str]) -> bool:
    if str_or_pattern is None or input is None:
        return False

    if isinstance(str_or_pattern, str):
        exact_match_str: str = str_or_pattern
        return input == exact_match_str
    elif isinstance(str_or_pattern, Pattern):
        pattern: Pattern = str_or_pattern
        return pattern.search(input) is not None
    else:
        raise BoltError(f"{str_or_pattern} ({type(str_or_pattern)}) must be either str or Pattern")
