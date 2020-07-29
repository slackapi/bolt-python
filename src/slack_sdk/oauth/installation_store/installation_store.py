from abc import abstractmethod
from typing import Optional

from .models.installation import Installation


class InstallationStore():

    @abstractmethod
    def save(self, installation: Installation):
        raise NotImplementedError

    @abstractmethod
    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
    ) -> Optional[Installation]:
        raise NotImplementedError
