from typing import Any


def get_kwargs_for_logging(self: Any) -> str:
    separator = "', '"
    return f"'{separator.join(self.__call__.__kwdefaults__.keys())}' or no arguments"


def get_name_for_logging(self: Any) -> str:
    return f"{self.__class__.__name__.lower()}()"
