from typing import Any


def _can_complete(self: Any) -> bool:
    return hasattr(self, "client") and self.client is not None and self.function_execution_id is not None
