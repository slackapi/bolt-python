#!/usr/bin/env python
import os
from .error import CliError
from .utils import handle_exception


json_file_name = "manifest.json"


@handle_exception
def get_manifest(working_directory):
    file_path = f"{working_directory}/{json_file_name}"

    if not os.path.exists(file_path):
        raise CliError(f"Manifest file not found!\nPath: {file_path}")

    with open(file_path, "r") as manifest:
        return manifest.read()


if __name__ == "__main__":
    current_wd = os.getcwd()
    print(get_manifest(current_wd))
