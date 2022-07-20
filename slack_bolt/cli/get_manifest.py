#!/usr/bin/env python
import os
from .hook_utils.errors import handle_exception, CliError


file_name = "manifest"
json_file_name = f"{file_name}.json"
# py_file_name = "{file_name}.py"


@handle_exception
def get_manifest(working_directory):
    file_path = f"{working_directory}/{json_file_name}"

    if not os.path.exists(file_path):
        raise CliError(f"Manifest file not found!\nPath: {file_path}")

    with open(file_path, "r") as manifest:
        return manifest.read()


def main():
    current_wd = os.getcwd()
    print(get_manifest(current_wd))
