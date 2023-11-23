#!/usr/bin/env python
import os
import re
import sys
from typing import List

from .error import CliError
from .protocol import Protocol, protocol_factory

PROTOCOL: Protocol

EXCLUDED_DIRECTORIES = [
    "lib",
    "bin",
    "include",
    "node_modules",
    "packages",
    "logs",
    "build",
    "coverage",
    "target",
    "tmp",
    "test",
    "tests",
]

DIRECTORY_IGNORE_REGEX = re.compile(r"(^\.|^\_|^{}$)".format("$|^".join(EXCLUDED_DIRECTORIES)), re.IGNORECASE)


def filter_directories(directories: List[str]) -> List[str]:
    return [directory for directory in directories if not DIRECTORY_IGNORE_REGEX.match(directory)]


def find_file_path(path: str, file: str) -> str:
    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        dirs[:] = filter_directories(dirs)
        if file in files:
            return os.path.join(root, file)
    raise CliError(f"Could not find a manifest.json file")


def get_manifest(working_directory: str) -> str:
    file_path = find_file_path(working_directory, f"manifest.json")

    with open(file_path, "r") as manifest:
        return manifest.read()


if __name__ == "__main__":
    PROTOCOL = protocol_factory()
    PROTOCOL.respond(get_manifest(os.getcwd()))
