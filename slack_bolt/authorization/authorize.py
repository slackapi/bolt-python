import inspect
from logging import Logger
from typing import Optional, Callable, Dict, Any

from slack_sdk.errors import SlackApiError
from slack_sdk.oauth import InstallationStore
from slack_sdk.oauth.installation_store import Bot

from slack_bolt.authorization.authorize_args import AuthorizeArgs
from slack_bolt.authorization.authorize_result import AuthorizeResult
from slack_bolt.context.context import BoltContext


class Authorize:
    def __init__(self):
        pass

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: str,
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        raise NotImplementedError()


class CallableAuthorize(Authorize):
    def __init__(
        self, *, logger: Logger, func: Callable[..., AuthorizeResult],
    ):
        self.logger = logger
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: str,
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
    authorize_result_cache: Dict[str, AuthorizeResult] = {}

    def __init__(
        self,
        *,
        logger: Logger,
        installation_store: InstallationStore,
        cache_enabled: bool = False,
    ):
        self.logger = logger
        self.installation_store = installation_store
        self.cache_enabled = cache_enabled

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: str,
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        bot: Optional[Bot] = self.installation_store.find_bot(
            enterprise_id=enterprise_id, team_id=team_id,
        )
        if bot is None:
            self.logger.debug(
                f"No installation data found "
                f"for enterprise_id: {enterprise_id} team_id: {team_id}"
            )
            return None

        if self.cache_enabled and bot.bot_token in self.authorize_result_cache:
            return self.authorize_result_cache[bot.bot_token]
        try:
            auth_result = context.client.auth_test(token=bot.bot_token)
            authorize_result = AuthorizeResult.from_auth_test_response(
                auth_test_response=auth_result,
                bot_token=bot.bot_token,
                user_token=None,  # Not yet supported
            )
            if self.cache_enabled:
                self.authorize_result_cache[bot.bot_token] = authorize_result
            return authorize_result
        except SlackApiError as err:
            self.logger.debug(
                f"The stored bot token for enterprise_id: {enterprise_id} team_id: {team_id} "
                f"is no longer valid. (response: {err.response})"
            )
            return None
