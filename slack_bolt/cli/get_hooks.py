#!/usr/bin/env python
import json


hook_payload = {
    "hooks": {
        "get-manifest": "get-manifest",
        "start": "start",
    },
    "config": {
        "watch": {
            "filter-regex": "^manifest\\.(ts|js|json)$",
            "paths": [
                "."
            ]
        },
        "sdk-managed-connection-enabled": True,
    }
}


def main():
  print(json.dumps(hook_payload))
