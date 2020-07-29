from abc import abstractmethod
from logging import Logger
from typing import Optional

from .models.bot import Bot
from .models.installation import Installation


class InstallationStore():
    def __init__(self, logger: Optional[Logger] = None):
        self.logger: Optional[Logger] = logger

    @abstractmethod
    def save(self, installation: Installation):
        raise NotImplementedError

    @abstractmethod
    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
    ) -> Optional[Bot]:
        raise NotImplementedError
