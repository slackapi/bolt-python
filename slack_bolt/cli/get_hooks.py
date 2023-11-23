#!/usr/bin/env python
import json
from .protocol import Protocol, MessageBoundaryProtocol, DefaultProtocol, protocol_factory

PROTOCOL: Protocol

hooks_payload = {
    "hooks": {
        "get-manifest": "python -m slack_bolt.cli.get_manifest",
        "start": "python -m slack_bolt.cli.start",
    },
    "config": {
        "watcher": {"filter-regex": "^manifest\\.(json)$", "paths": ["."]},
        "protocol-version": [MessageBoundaryProtocol.name, DefaultProtocol.name],
        "sdk-managed-connection-enabled": True,
    },
}

if __name__ == "__main__":
    PROTOCOL = protocol_factory()
    PROTOCOL.respond(json.dumps(hooks_payload))
