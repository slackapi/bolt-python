from typing import Any


def can_not_complete(self: Any) -> bool:
    return not hasattr(self, "client") or self.client is None or self.function_execution_id is None


def get_kwargs_for_logging(self: Any) -> str:
    separator = "', '"
    return f"'{separator.join(self.__call__.__kwdefaults__.keys())}' or no arguments"


def get_name_for_logging(self: Any) -> str:
    return f"{self.__class__.__name__.lower()}()"
