import os


def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    for key, value in old_env.items():
        if key.startswith("BOLT_PYTHON_"):
            os.environ[key] = value
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)


def get_mock_server_mode() -> str:
    """Returns a str representing the mode.

    :return: threading/multiprocessing
    """
    mode = os.environ.get("BOLT_PYTHON_MOCK_SERVER_MODE")
    if mode is None:
        return "multiprocessing"
    else:
        return mode
