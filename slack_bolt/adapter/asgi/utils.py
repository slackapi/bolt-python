from typing import Iterable, Tuple, Union, Dict

scope_value_type = Union[str, bytes, Iterable[Tuple[bytes, bytes]]]

scope_type = Dict[str, scope_value_type]
