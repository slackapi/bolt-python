import asyncio
import json
import logging
from time import time
from urllib.parse import quote

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import SlackResponse
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.workflows.step.async_step import AsyncWorkflowStep
from slack_bolt.workflows.step.utilities.async_complete import AsyncComplete
from slack_bolt.workflows.step.utilities.async_configure import AsyncConfigure
from slack_bolt.workflows.step.utilities.async_fail import AsyncFail
from slack_bolt.workflows.step.utilities.async_update import AsyncUpdate
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncWorkflowStepsDecorator:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    @pytest.fixture
    def event_loop(self):
        old_os_env = remove_os_env_temporarily()
        try:
            setup_mock_web_api_server(self)
            self.app = AsyncApp(
                client=self.web_client, signing_secret=self.signing_secret
            )
            self.app.step(copy_review_step)

            loop = asyncio.get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server(self)
        finally:
            restore_os_env(old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    @pytest.mark.asyncio
    async def test_edit(self):
        timestamp, body = str(int(time())), f"payload={quote(json.dumps(edit_payload))}"
        headers = {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }
        request = AsyncBoltRequest(body=body, headers=headers)
        response = await self.app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1

        self.app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        self.app.step(
            callback_id="copy_review___", edit=edit, save=save, execute=execute
        )
        response = await self.app.async_dispatch(request)
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_save(self):
        timestamp, body = str(int(time())), f"payload={quote(json.dumps(save_payload))}"
        headers = {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }
        request = AsyncBoltRequest(body=body, headers=headers)
        response = await self.app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1

        self.app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        self.app.step(
            callback_id="copy_review___", edit=edit, save=save, execute=execute
        )
        response = await self.app.async_dispatch(request)
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_execute(self):
        timestamp, body = str(int(time())), json.dumps(execute_payload)
        headers = {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }
        request = AsyncBoltRequest(body=body, headers=headers)
        response = await self.app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        await asyncio.sleep(0.5)
        assert self.mock_received_requests["/workflows.stepCompleted"] == 1

        self.app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        self.app.step(
            callback_id="copy_review___", edit=edit, save=save, execute=execute
        )
        response = await self.app.async_dispatch(request)
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_logger_propagation(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
            logger=custom_logger,
        )
        app.step(logger_test_step)

        timestamp, body = str(int(time())), f"payload={quote(json.dumps(edit_payload))}"
        headers = {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }
        request = AsyncBoltRequest(body=body, headers=headers)
        response = await self.app.async_dispatch(request)
        assert response.status == 200

        timestamp, body = str(int(time())), f"payload={quote(json.dumps(save_payload))}"
        headers = {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }
        request = AsyncBoltRequest(body=body, headers=headers)
        response = await self.app.async_dispatch(request)
        assert response.status == 200

        timestamp, body = str(int(time())), json.dumps(execute_payload)
        headers = {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }
        request = AsyncBoltRequest(body=body, headers=headers)
        response = await self.app.async_dispatch(request)
        assert response.status == 200
        await asyncio.sleep(0.5)  # wait for the completion


edit_payload = {
    "type": "workflow_step_edit",
    "token": "verification-token",
    "action_ts": "1601541356.268786",
    "team": {
        "id": "T111",
        "domain": "subdomain",
        "enterprise_id": "E111",
        "enterprise_name": "Org Name",
    },
    "user": {"id": "W111", "username": "primary-owner", "team_id": "T111"},
    "callback_id": "copy_review",
    "trigger_id": "111.222.xxx",
    "workflow_step": {
        "workflow_id": "12345",
        "step_id": "111-222-333-444-555",
        "inputs": {
            "taskAuthorEmail": {"value": "seratch@example.com"},
            "taskDescription": {"value": "This is the task for you!"},
            "taskName": {"value": "The important task"},
        },
        "outputs": [
            {"name": "taskName", "type": "text", "label": "Task Name"},
            {"name": "taskDescription", "type": "text", "label": "Task Description"},
            {"name": "taskAuthorEmail", "type": "text", "label": "Task Author Email"},
        ],
    },
}

save_payload = {
    "type": "view_submission",
    "team": {
        "id": "T111",
        "domain": "subdomain",
        "enterprise_id": "E111",
        "enterprise_name": "Org Name",
    },
    "user": {
        "id": "W111",
        "username": "primary-owner",
        "name": "primary-owner",
        "team_id": "T111",
    },
    "api_app_id": "A111",
    "token": "verification-token",
    "trigger_id": "111.222.xxx",
    "view": {
        "id": "V111",
        "team_id": "T111",
        "type": "workflow_step",
        "blocks": [
            {
                "type": "section",
                "block_id": "intro-section",
                "text": {
                    "type": "plain_text",
                    "text": "Create a task in one of the listed projects. The link to the task and other details will be available as variable data in later steps.",
                },
            },
            {
                "type": "input",
                "block_id": "task_name_input",
                "label": {"type": "plain_text", "text": "Task name"},
                "optional": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_name",
                    "placeholder": {"type": "plain_text", "text": "Write a task name"},
                },
            },
            {
                "type": "input",
                "block_id": "task_description_input",
                "label": {"type": "plain_text", "text": "Task description"},
                "optional": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_description",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Write a description for your task",
                    },
                },
            },
            {
                "type": "input",
                "block_id": "task_author_input",
                "label": {"type": "plain_text", "text": "Task author"},
                "optional": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_author",
                    "placeholder": {"type": "plain_text", "text": "Write a task name"},
                },
            },
        ],
        "private_metadata": "",
        "callback_id": "copy_review",
        "state": {
            "values": {
                "task_name_input": {
                    "task_name": {
                        "type": "plain_text_input",
                        "value": "The important task",
                    }
                },
                "task_description_input": {
                    "task_description": {
                        "type": "plain_text_input",
                        "value": "This is the task for you!",
                    }
                },
                "task_author_input": {
                    "task_author": {
                        "type": "plain_text_input",
                        "value": "seratch@example.com",
                    }
                },
            }
        },
        "hash": "111.zzz",
        "submit_disabled": False,
        "app_id": "A111",
        "external_id": "",
        "app_installed_team_id": "T111",
        "bot_id": "B111",
    },
    "response_urls": [],
    "workflow_step": {
        "workflow_step_edit_id": "111.222.zzz",
        "workflow_id": "12345",
        "step_id": "111-222-333-444-555",
    },
}

execute_payload = {
    "token": "verification-token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "type": "workflow_step_execute",
        "callback_id": "copy_review",
        "workflow_step": {
            "workflow_step_execute_id": "zzz-execution",
            "workflow_id": "12345",
            "workflow_instance_id": "11111",
            "step_id": "111-222-333-444-555",
            "inputs": {
                "taskAuthorEmail": {"value": "ksera@slack-corp.com"},
                "taskDescription": {"value": "sdfsdf"},
                "taskName": {"value": "a"},
            },
            "outputs": [
                {"name": "taskName", "type": "text", "label": "Task Name"},
                {
                    "name": "taskDescription",
                    "type": "text",
                    "label": "Task Description",
                },
                {
                    "name": "taskAuthorEmail",
                    "type": "text",
                    "label": "Task Author Email",
                },
            ],
        },
        "event_ts": "1601541373.225894",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1601541373,
}

#
# The normal pattern tests
#

# https://api.slack.com/tutorials/workflow-builder-steps

copy_review_step = AsyncWorkflowStep.builder("copy_review")


async def noop_middleware(next):
    return await next()


@copy_review_step.edit(middleware=[noop_middleware])
async def edit(ack: AsyncAck, step, configure: AsyncConfigure):
    assert step is not None
    await ack()
    await configure(
        blocks=[
            {
                "type": "section",
                "block_id": "intro-section",
                "text": {
                    "type": "plain_text",
                    "text": "Create a task in one of the listed projects. The link to the task and other details will be available as variable data in later steps.",
                },
            },
            {
                "type": "input",
                "block_id": "task_name_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_name",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Write a task name",
                    },
                },
                "label": {"type": "plain_text", "text": "Task name"},
            },
            {
                "type": "input",
                "block_id": "task_description_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_description",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Write a description for your task",
                    },
                },
                "label": {"type": "plain_text", "text": "Task description"},
            },
            {
                "type": "input",
                "block_id": "task_author_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_author",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Write a task name",
                    },
                },
                "label": {"type": "plain_text", "text": "Task author"},
            },
        ]
    )


@copy_review_step.save(middleware=[noop_middleware])
async def save(ack: AsyncAck, step: dict, view: dict, update: AsyncUpdate):
    assert step is not None
    assert view is not None
    state_values = view["state"]["values"]
    await update(
        inputs={
            "taskName": {
                "value": state_values["task_name_input"]["task_name"]["value"],
            },
            "taskDescription": {
                "value": state_values["task_description_input"]["task_description"][
                    "value"
                ],
            },
            "taskAuthorEmail": {
                "value": state_values["task_author_input"]["task_author"]["value"],
            },
        },
        outputs=[
            {
                "name": "taskName",
                "type": "text",
                "label": "Task Name",
            },
            {
                "name": "taskDescription",
                "type": "text",
                "label": "Task Description",
            },
            {
                "name": "taskAuthorEmail",
                "type": "text",
                "label": "Task Author Email",
            },
        ],
    )
    await ack()


pseudo_database = {}


@copy_review_step.execute(middleware=[noop_middleware])
async def execute(
    step: dict, client: AsyncWebClient, complete: AsyncComplete, fail: AsyncFail
):
    assert step is not None
    try:
        await complete(
            outputs={
                "taskName": step["inputs"]["taskName"]["value"],
                "taskDescription": step["inputs"]["taskDescription"]["value"],
                "taskAuthorEmail": step["inputs"]["taskAuthorEmail"]["value"],
            }
        )

        user: SlackResponse = await client.users_lookupByEmail(
            email=step["inputs"]["taskAuthorEmail"]["value"]
        )
        user_id = user["user"]["id"]
        new_task = {
            "task_name": step["inputs"]["taskName"]["value"],
            "task_description": step["inputs"]["taskDescription"]["value"],
        }
        tasks = pseudo_database.get(user_id, [])
        tasks.append(new_task)
        pseudo_database[user_id] = tasks

        blocks = []
        for task in tasks:
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": task["task_name"]},
                }
            )
            blocks.append({"type": "divider"})

        await client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "title": {"type": "plain_text", "text": "Your tasks!"},
                "blocks": blocks,
            },
        )
    except Exception as err:
        await fail(error={"message": f"Something wrong! {err}"})


#
# Logger propagation tests
#

import time
custom_logger = logging.getLogger(f"{__name__}-{time.time()}-async-logger-test")
custom_logger.setLevel(logging.INFO)
added_handler = logging.NullHandler()
custom_logger.addHandler(added_handler)
added_filter = logging.Filter()
custom_logger.addFilter(added_filter)

logger_test_step = AsyncWorkflowStep.builder(
    "copy_review",
    base_logger=custom_logger,  # to pass this logger to middleware / middleware matchers
)


def _verify_logger(logger: logging.Logger):
    assert logger.level == custom_logger.level
    assert len(logger.handlers) == len(custom_logger.handlers)
    assert logger.handlers[-1] == custom_logger.handlers[-1]
    assert len(logger.filters) == len(custom_logger.filters)
    assert logger.filters[-1] == custom_logger.filters[-1]


async def logger_middleware(next, logger):
    _verify_logger(logger)
    await next()


async def logger_matcher(logger):
    _verify_logger(logger)
    return True


@logger_test_step.edit(
    middleware=[logger_middleware],
    matchers=[logger_matcher],
)
async def edit_for_logger_test(ack: AsyncAck, logger: logging.Logger):
    _verify_logger(logger)
    await ack()


@logger_test_step.save(
    middleware=[logger_middleware],
    matchers=[logger_matcher],
)
async def save_for_logger_test(ack: AsyncAck, logger: logging.Logger):
    _verify_logger(logger)
    await ack()


@logger_test_step.execute(
    middleware=[logger_middleware],
    matchers=[logger_matcher],
)
async def execute_for_logger_test(logger: logging.Logger):
    _verify_logger(logger)
