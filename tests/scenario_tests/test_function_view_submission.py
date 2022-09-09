body = {
    "type": "view_submission",
    "team": {"id": "T111", "domain": "workspace-domain"},
    "enterprise": None,
    "user": {"id": "U111", "name": "primary-owner", "team_id": "T111"},
    "view": {
        "id": "V111",
        "team_id": "T111",
        "app_id": "A111",
        "app_installed_team_id": "T111",
        "bot_id": "B111",
        "title": {"type": "plain_text", "text": "Sample modal title", "emoji": True},
        "type": "modal",
        "blocks": [
            {
                "type": "input",
                "block_id": "input_block_id",
                "label": {"type": "plain_text", "text": "What are your hopes and dreams?", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sample_input_id",
                    "multiline": True,
                    "dispatch_action_config": {"trigger_actions_on": ["on_enter_pressed"]},
                },
            }
        ],
        "close": None,
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "state": {"values": {"input_block_id": {"sample_input_id": {"type": "plain_text_input", "value": "hello world"}}}},
        "hash": "123.abc",
        "private_metadata": "",
        "callback_id": "func_sample_view_id",
        "root_view_id": "V111",
        "previous_view_id": None,
        "clear_on_close": False,
        "notify_on_close": True,
        "external_id": "",
    },
    "api_app_id": "A111",
    "response_urls": [],
    "bot_access_token": "xwfp-111",
    "function_data": {
        "execution_id": "Fx111",
        "function": {"callback_id": "sample_view_function"},
        "inputs": {
            "interactivity": {
                "interactor": {
                    "id": "U111",
                    "secret": "NDA111",
                },
                "interactivity_pointer": "123.123.acb1",
            },
            "interactivity.interactor": {
                "id": "U111",
                "secret": "NDA111",
            },
            "interactivity.interactor.id": "U111",
            "interactivity.interactor.secret": "NDA111",
            "interactivity.interactivity_pointer": "123.123.acb1",
        },
    },
    "interactivity": {
        "interactor": {
            "secret": "NDA111",
            "id": "U111",
        },
        "interactivity_pointer": "123.123.acb1",
    },
}
