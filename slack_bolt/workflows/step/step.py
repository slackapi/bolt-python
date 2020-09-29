from typing import Callable, Union, Optional

from slack_bolt.context import BoltContext
from slack_bolt.listener import Listener, CustomListener
from slack_bolt.listener_matcher.builtins import (
    workflow_step_edit,
    workflow_step_save,
    workflow_step_execute,
)
from slack_bolt.middleware import CustomMiddleware
from slack_bolt.response import BoltResponse
from slack_bolt.workflows.step.utilities.complete import Complete
from slack_bolt.workflows.step.utilities.configure import Configure
from slack_bolt.workflows.step.utilities.fail import Fail
from slack_bolt.workflows.step.utilities.update import Update
from slack_sdk.web import WebClient


class WorkflowStep:
    callback_id: str
    edit: Listener
    save: Listener
    execute: Listener

    def __init__(
        self,
        *,
        callback_id: str,
        edit: Union[Callable[..., Optional[BoltResponse]], Listener],
        save: Union[Callable[..., Optional[BoltResponse]], Listener],
        execute: Union[Callable[..., Optional[BoltResponse]], Listener],
        app_name: Optional[str] = None,
    ):
        self.callback_id = callback_id
        app_name = app_name or __name__
        self.edit = self._build_listener(callback_id, app_name, edit, "edit")
        self.save = self._build_listener(callback_id, app_name, save, "save")
        self.execute = self._build_listener(
            callback_id, app_name, execute, "execute")

    @classmethod
    def _build_listener(cls, callback_id, app_name, listener, name):
        if isinstance(listener, Listener):
            return listener
        elif isinstance(listener, Callable):
            return CustomListener(
                app_name=app_name,
                matchers=cls._build_matchers(name, callback_id),
                middleware=cls._build_middleware(name, callback_id),
                ack_function=listener,
                lazy_functions=[],
                auto_acknowledgement=name == "execute",
            )
        else:
            raise ValueError(f"Invalid `{name}` listener")

    @classmethod
    def _build_matchers(cls, name, callback_id):
        if name == "edit":
            return [workflow_step_edit(callback_id)]
        elif name == "save":
            return [workflow_step_save(callback_id)]
        elif name == "execute":
            return [workflow_step_execute()]
        else:
            raise ValueError(f"Invalid name {name}")

    @classmethod
    def _build_middleware(cls, name, callback_id):
        if name == "edit":
            return [_build_edit_listener_middleware(callback_id)]
        elif name == "save":
            return [_build_save_listener_middleware()]
        elif name == "execute":
            return [_build_execute_listener_middleware()]
        else:
            raise ValueError(f"Invalid name {name}")


#######################
# Edit
#######################


def _build_edit_listener_middleware(callback_id):
    def edit_listener_middleware(
        context: BoltContext,
        client: WebClient,
        body: dict,
        next: Callable[[], BoltResponse],
    ):
        context["configure"] = Configure(
            callback_id=callback_id, client=client, body=body,
        )
        return next()

    return CustomMiddleware(app_name=__name__, func=edit_listener_middleware)


#######################
# Save
#######################


def _build_save_listener_middleware():
    def save_listener_middleware(
        context: BoltContext,
        client: WebClient,
        body: dict,
        next: Callable[[], BoltResponse],
    ):
        context["update"] = Update(client=client, body=body,)
        return next()

    return CustomMiddleware(app_name=__name__, func=save_listener_middleware)


#######################
# Execute
#######################


def _build_execute_listener_middleware():
    def execute_listener_middleware(
        context: BoltContext,
        client: WebClient,
        body: dict,
        next: Callable[[], BoltResponse],
    ):
        context["complete"] = Complete(client=client, body=body,)
        context["fail"] = Fail(client=client, body=body,)
        return next()

    return CustomMiddleware(app_name=__name__, func=execute_listener_middleware)
