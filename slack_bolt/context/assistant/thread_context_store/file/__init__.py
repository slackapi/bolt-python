import json
from typing import Optional, Dict, Union
from pathlib import Path

from ..store import AssistantThreadContextStore, AssistantThreadContext


class FileAssistantThreadContextStore(AssistantThreadContextStore):

    def __init__(
        self,
        base_dir: str = str(Path.home()) + "/.bolt-app-assistant-thread-contexts",
    ):
        self.base_dir = base_dir
        self._mkdir(self.base_dir)

    def save(self, *, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None:
        path = f"{self.base_dir}/{channel_id}-{thread_ts}.json"
        with open(path, "w") as f:
            f.write(json.dumps(context))

    def find(self, *, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]:
        path = f"{self.base_dir}/{channel_id}-{thread_ts}.json"
        try:
            with open(path) as f:
                data = json.loads(f.read())
                if data.get("channel_id") is not None:
                    return AssistantThreadContext(data)
        except FileNotFoundError:
            pass
        return None

    @staticmethod
    def _mkdir(path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
