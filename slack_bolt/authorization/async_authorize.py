import inspect
from logging import Logger
from typing import Optional, Callable, Awaitable, Dict, Any

from slack_sdk.errors import SlackApiError
from slack_sdk.oauth.installation_store import Bot
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)

from slack_bolt.authorization.async_authorize_args import AsyncAuthorizeArgs
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.context.async_context import AsyncBoltContext


class AsyncAuthorize:
    def __init__(self):
        pass

    async def __call__(
        self,
        *,
        context: AsyncBoltContext,
        enterprise_id: Optional[str],
        team_id: str,
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        raise NotImplementedError()


class AsyncCallableAuthorize(AsyncAuthorize):
    def __init__(
        self, *, logger: Logger, func: Callable[..., Awaitable[AuthorizeResult]]
    ):
        self.logger = logger
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args

    async def __call__(
        self,
        *,
        context: AsyncBoltContext,
        enterprise_id: Optional[str],
        team_id: str,
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        try:
            all_available_args = {
                "args": AsyncAuthorizeArgs(
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

            auth_result: Optional[AuthorizeResult] = await self.func(**kwargs)
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


class AsyncInstallationStoreAuthorize(AsyncAuthorize):
    def __init__(
        self, *, logger: Logger, installation_store: AsyncInstallationStore,
    ):
        self.logger = logger
        self.installation_store = installation_store

    async def __call__(
        self,
        *,
        context: AsyncBoltContext,
        enterprise_id: Optional[str],
        team_id: str,
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        bot: Optional[Bot] = await self.installation_store.async_find_bot(
            enterprise_id=enterprise_id, team_id=team_id,
        )
        if bot is None:
            self.logger.debug(
                f"No installation data found "
                f"for enterprise_id: {enterprise_id} team_id: {team_id}"
            )
            return None

        try:
            auth_result = await context.client.auth_test(token=bot.bot_token)
            return AuthorizeResult.from_auth_test_response(
                auth_test_response=auth_result,
                bot_token=bot.bot_token,
                user_token=None,  # Not yet supported
            )
        except SlackApiError as err:
            self.logger.debug(
                f"The stored bot token for enterprise_id: {enterprise_id} team_id: {team_id} "
                f"is no longer valid. (response: {err.response})"
            )
            return None
