#!/usr/bin/env python
import os
import re
from ..error import CliError
from .utils import handle_exceptions
from typing import List

FILE = "manifest"

EXPLICIT_EXCLUDED_DIRECTORIES = [
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

DIRECTORY_IGNORE_REGEX = re.compile(r"(^\.|^\_|^{}$)".format("$|^".join(EXPLICIT_EXCLUDED_DIRECTORIES)), re.IGNORECASE)


def filter_directories(directories: List[str]) -> List[str]:
    return [directory for directory in directories if not DIRECTORY_IGNORE_REGEX.match(directory)]


def find_file_path(path: str, file: str) -> str:
    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        dirs[:] = filter_directories(dirs)
        if file in files:
            return os.path.join(root, file)
    raise CliError(f"Manifest file not found!\nPath: {path}\nFile: {file}")


@handle_exceptions()
def get_manifest(working_directory: str) -> str:
    file_path = find_file_path(working_directory, f"{FILE}.json")

    print(file_path)
    with open(file_path, "r") as manifest:
        return manifest.read()


if __name__ == "__main__":
    current_wd = os.getcwd()
    print(get_manifest(current_wd))
