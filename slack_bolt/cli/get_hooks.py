#!/usr/bin/env python
import json


hook_payload = {
    "hooks": {
        "get-manifest": "python -m slack_bolt.cli.get_manifest",
        "start": "python -m slack_bolt.cli.start",
    },
    "config": {
        "watch": {"filter-regex": "^manifest\\.(json)$", "paths": ["."]},
        "sdk-managed-connection-enabled": True,
    },
}


def main() -> None:
    print(json.dumps(hook_payload))
