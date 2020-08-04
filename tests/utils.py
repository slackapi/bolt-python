import os


def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)
