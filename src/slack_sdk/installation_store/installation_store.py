from typing import Optional

from .installation import Installation


class InstallationStore():

    def save(self, installation: Installation):
        raise NotImplementedError

    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
    ) -> Optional[Installation]:
        raise NotImplementedError
