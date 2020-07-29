import json
from logging import Logger
from pathlib import Path
from typing import Optional, Union

from slack_sdk.oauth.installation_store.installation_store import InstallationStore
from slack_sdk.oauth.installation_store.models.bot import Bot
from slack_sdk.oauth.installation_store.models.installation import Installation


class FileInstallationStore(InstallationStore):

    def __init__(
        self,
        *,
        logger: Logger,
        base_dir: str = str(Path.home()) + "/.bolt-app-installation",
        historical_data_enabled: bool = True,
        client_id: Optional[str] = None,
    ):
        self.logger = logger
        self.base_dir = base_dir
        self.historical_data_enabled = historical_data_enabled
        self.client_id = client_id
        if self.client_id is not None:
            self.base_dir = f"{self.base_dir}/{self.client_id}"

    def save(self, installation: Installation):
        none = "none"
        e_id = installation.enterprise_id or none
        t_id = installation.team_id or none
        team_installation_dir = f"{self.base_dir}/{e_id}-{t_id}"
        self._mkdir(team_installation_dir)

        if self.historical_data_enabled:
            history_version: str = str(installation.installed_at)

            entity: str = json.dumps(installation.to_bot().__dict__)
            with open(f"{team_installation_dir}/bot-latest", "w") as f:
                f.write(entity)
            with open(f"{team_installation_dir}/bot-{history_version}", "w") as f:
                f.write(entity)

            u_id = installation.user_id or none
            entity: str = json.dumps(installation.__dict__)
            with open(f"{team_installation_dir}/installer-{u_id}-latest", "w") as f:
                f.write(entity)
            with open(f"{team_installation_dir}/installer-{u_id}-{history_version}", "w") as f:
                f.write(entity)

        else:
            with open(f"{team_installation_dir}/bot-latest", "w") as f:
                entity: str = json.dumps(installation.to_bot().__dict__)
                f.write(entity)

            u_id = installation.user_id or none
            installer_filepath = f"{team_installation_dir}/installer-{u_id}-latest"
            with open(installer_filepath, "w") as f:
                entity: str = json.dumps(installation.__dict__)
                f.write(entity)

    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
    ) -> Optional[Installation]:
        # TODO: org-apps support
        none = "none"
        e_id = enterprise_id or none
        t_id = team_id or none
        bot_filepath = f"{self.base_dir}/{e_id}-{t_id}/bot-latest"
        try:
            with open(bot_filepath) as f:
                data = json.loads(f.read())
                return Bot(**data)
        except FileNotFoundError as e:
            message = f"Failed to find bot installation data for enterprise: {e_id}, team: {t_id}: {e}"
            self.logger.warning(message)
            return None

    @staticmethod
    def _mkdir(path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
