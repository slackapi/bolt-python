from typing import Any


def can_not_complete(self: Any) -> bool:
    return not hasattr(self, "client") or self.client is None or self.function_execution_id is None
