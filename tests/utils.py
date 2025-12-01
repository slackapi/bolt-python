import os
import asyncio


def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    for key, value in old_env.items():
        if key.startswith("BOLT_PYTHON_"):
            os.environ[key] = value
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)
