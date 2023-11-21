#!/usr/bin/env python
import json

hooks_payload = {
    "hooks": {
        "get-manifest": "python -m slack_bolt.cli.get_manifest",
        "start": "python -m slack_bolt.cli.start",
    },
    "config": {
        "watcher": {"filter-regex": "^manifest\\.(json)$", "paths": ["."]},
        "sdk-managed-connection-enabled": True,
    },
}

if __name__ == "__main__":
    print(json.dumps(hooks_payload))
