#!/usr/bin/env python
import json
from .protocol import Protocol, MessageBoundaryProtocol, DefaultProtocol, protocol_factory
from slack_bolt.cli import get_manifest, start

PROTOCOL: Protocol

hooks_payload = {
    "hooks": {
        "get-manifest": f"python -m {get_manifest.__name__}",
        "start": f"python -m {start.__name__}",
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
