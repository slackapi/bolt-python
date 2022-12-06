from typing import TypedDict, Iterable, ByteString, Tuple


class ScopeType(TypedDict):
    type: str
    method: str
    path: str
    query_string: ByteString
    headers: Iterable[Tuple[ByteString, ByteString]]
