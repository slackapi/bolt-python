import inspect
from logging import Logger
from typing import Optional, Callable, Dict, Any

from slack_sdk.errors import SlackApiError
from slack_sdk.oauth import InstallationStore
from slack_sdk.oauth.installation_store import Bot
from slack_sdk.oauth.installation_store.models.installation import Installation
from slack_sdk.oauth.token_rotation.rotator import TokenRotator

from slack_bolt.authorization.authorize_args import AuthorizeArgs
from slack_bolt.authorization.authorize_result import AuthorizeResult
from slack_bolt.context.context import BoltContext
from slack_bolt.error import BoltError


class Authorize:
    """This provides authorize function that returns AuthorizeResult
    for an incoming request from Slack."""

    def __init__(self):
        pass

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: Optional[str],  # can be None for org-wide installed apps
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        raise NotImplementedError()


class CallableAuthorize(Authorize):
    """When you pass the authorize argument in AsyncApp constructor,
    This authorize implementation will be used.
    """

    def __init__(
        self,
        *,
        logger: Logger,
        func: Callable[..., AuthorizeResult],
    ):
        self.logger = logger
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: Optional[str],  # can be None for org-wide installed apps
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        try:
            all_available_args = {
                "args": AuthorizeArgs(
                    context=context,
                    enterprise_id=enterprise_id,
                    team_id=team_id,
                    user_id=user_id,
                ),
                "logger": context.logger,
                "client": context.client,
                "context": context,
                "enterprise_id": enterprise_id,
                "team_id": team_id,
                "user_id": user_id,
            }
            for k, v in context.items():
                if k not in all_available_args:
                    all_available_args[k] = v

            kwargs: Dict[str, Any] = {  # type: ignore
                k: v for k, v in all_available_args.items() if k in self.arg_names  # type: ignore
            }
            found_arg_names = kwargs.keys()
            for name in self.arg_names:
                if name not in found_arg_names:
                    self.logger.warning(f"{name} is not a valid argument")
                    kwargs[name] = None

            auth_result = self.func(**kwargs)
            if auth_result is None:
                return auth_result

            if isinstance(auth_result, AuthorizeResult):
                return auth_result
            else:
                raise ValueError(
                    f"Unexpected returned value from authorize function (type: {type(auth_result)})"
                )
        except SlackApiError as err:
            self.logger.debug(
                f"The stored bot token for enterprise_id: {enterprise_id} team_id: {team_id} "
                f"is no longer valid. (response: {err.response})"
            )
            return None


class InstallationStoreAuthorize(Authorize):
    """If you use the OAuth flow settings, this authorize implementation will be used.
    As long as your own InstallationStore (or the built-in ones) works as you expect,
    you can expect that the authorize layer should work for you without any customization.
    """

    authorize_result_cache: Dict[str, AuthorizeResult]
    bot_only: bool
    find_installation_available: bool
    find_bot_available: bool
    token_rotator: Optional[TokenRotator]

    _config_error_message: str = (
        "InstallationStore with client_id/client_secret are required for token rotation"
    )

    def __init__(
        self,
        *,
        logger: Logger,
        installation_store: InstallationStore,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_rotation_expiration_minutes: Optional[int] = None,
        # For v1.0.x compatibility and people who still want its simplicity
        # use only InstallationStore#find_bot(enterprise_id, team_id)
        bot_only: bool = False,
        cache_enabled: bool = False,
    ):
        self.logger = logger
        self.installation_store = installation_store
        self.bot_only = bot_only
        self.cache_enabled = cache_enabled
        self.authorize_result_cache = {}
        self.find_installation_available = hasattr(
            installation_store, "find_installation"
        )
        self.find_bot_available = hasattr(installation_store, "find_bot")
        if client_id is not None and client_secret is not None:
            self.token_rotator = TokenRotator(
                client_id=client_id,
                client_secret=client_secret,
            )
        else:
            self.token_rotator = None
        self.token_rotation_expiration_minutes = (
            token_rotation_expiration_minutes or 120
        )

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: Optional[str],  # can be None for org-wide installed apps
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:

        bot_token: Optional[str] = None
        user_token: Optional[str] = None

        if not self.bot_only and self.find_installation_available:
            # Since v1.1, this is the default way.
            # If you want to use find_bot / delete_bot only, you can set bot_only as True.
            try:
                # Note that this is the latest information for the org/workspace.
                # The installer may not be the user associated with this incoming request.
                installation: Optional[
                    Installation
                ] = self.installation_store.find_installation(
                    enterprise_id=enterprise_id,
                    team_id=team_id,
                    is_enterprise_install=context.is_enterprise_install,
                )
                if installation is not None:
                    if installation.user_id != user_id:
                        # First off, remove the user token as the installer is a different user
                        installation.user_token = None
                        installation.user_scopes = []

                        # try to fetch the request user's installation
                        # to reflect the user's access token if exists
                        user_installation = self.installation_store.find_installation(
                            enterprise_id=enterprise_id,
                            team_id=team_id,
                            user_id=user_id,
                            is_enterprise_install=context.is_enterprise_install,
                        )
                        if user_installation is not None:
                            # Overwrite the installation with the one for this user
                            installation = user_installation

                    bot_token, user_token = (
                        installation.bot_token,
                        installation.user_token,
                    )
                    if (
                        installation.user_refresh_token is not None
                        or installation.bot_refresh_token is not None
                    ):
                        if self.token_rotator is None:
                            raise BoltError(self._config_error_message)
                        refreshed = self.token_rotator.perform_token_rotation(
                            installation=installation,
                            minutes_before_expiration=self.token_rotation_expiration_minutes,
                        )
                        if refreshed is not None:
                            self.installation_store.save(refreshed)
                            bot_token, user_token = (
                                refreshed.bot_token,
                                refreshed.user_token,
                            )

            except NotImplementedError as _:
                self.find_installation_available = False

        if (
            # If you intentionally use only find_bot / delete_bot,
            self.bot_only
            # If find_installation method is not available,
            or not self.find_installation_available
            # If find_installation did not return data and find_bot method is available,
            or (
                self.find_bot_available is True
                and bot_token is None
                and user_token is None
            )
        ):
            try:
                bot: Optional[Bot] = self.installation_store.find_bot(
                    enterprise_id=enterprise_id,
                    team_id=team_id,
                    is_enterprise_install=context.is_enterprise_install,
                )
                if bot is not None:
                    bot_token = bot.bot_token
                    if bot.bot_refresh_token is not None:
                        # Token rotation
                        if self.token_rotator is None:
                            raise BoltError(self._config_error_message)
                        refreshed = self.token_rotator.perform_bot_token_rotation(
                            bot=bot,
                            minutes_before_expiration=self.token_rotation_expiration_minutes,
                        )
                        if refreshed is not None:
                            self.installation_store.save_bot(refreshed)
                            bot_token = refreshed.bot_token

            except NotImplementedError as _:
                self.find_bot_available = False
            except Exception as e:
                self.logger.info(f"Failed to call find_bot method: {e}")

        token: Optional[str] = bot_token or user_token
        if token is None:
            # No valid token was found
            self._debug_log_for_not_found(enterprise_id, team_id)
            return None

        # Check cache to see if the bot object already exists
        if self.cache_enabled and token in self.authorize_result_cache:
            return self.authorize_result_cache[token]

        try:
            auth_test_api_response = context.client.auth_test(token=token)
            authorize_result = AuthorizeResult.from_auth_test_response(
                auth_test_response=auth_test_api_response,
                bot_token=bot_token,
                user_token=user_token,
            )
            if self.cache_enabled:
                self.authorize_result_cache[token] = authorize_result
            return authorize_result
        except SlackApiError as err:
            self.logger.debug(
                f"The stored bot token for enterprise_id: {enterprise_id} team_id: {team_id} "
                f"is no longer valid. (response: {err.response})"
            )
            return None

    # ------------------------------------------------

    def _debug_log_for_not_found(
        self, enterprise_id: Optional[str], team_id: Optional[str]
    ):
        self.logger.debug(
            "No installation data found "
            f"for enterprise_id: {enterprise_id} team_id: {team_id}"
        )
