from typing import Optional


def _can_say(self: any, channel: Optional[str]) -> bool:
    return (
        hasattr(self, "client")
        and self.client is not None
        and (channel or self.channel)
    )
