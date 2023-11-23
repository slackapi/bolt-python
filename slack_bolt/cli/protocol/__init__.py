import argparse
from .default_protocol import DefaultProtocol
from .message_boundary_protocol import MessageBoundaryProtocol
from .protocol import Protocol

__all__ = [
    "DefaultProtocol",
    "MessageBoundaryProtocol",
    "Protocol",
]


def protocol_factory() -> Protocol:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=str, required=False)
    parser.add_argument("--boundary", type=str, required=False)

    args, unknown = parser.parse_known_args()

    if args.protocol == MessageBoundaryProtocol.name:
        return MessageBoundaryProtocol(boundary=args.boundary)
    return DefaultProtocol()
