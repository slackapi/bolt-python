"""Cli modules to allow Bolt apps to interact with the bolt cli.
"""


def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("Shutdown requested... goodbye!")
        except Exception as e:
            print(e)
            exit()

    return wrapper
