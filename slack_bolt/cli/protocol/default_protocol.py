from .protocol import Protocol


class DefaultProtocol(Protocol):
    name: str = "default"

    def debug(self, msg: str, *args, **kwargs):
        """Nothing will be logged here"""
        pass

    def info(self, msg: str, *args, **kwargs):
        """Nothing will be logged here"""
        pass

    def warning(self, msg: str, *args, **kwargs):
        """Nothing will be logged here"""
        pass

    def error(self, msg: str, *args, **kwargs):
        """Nothing will be logged here"""
        pass

    def respond(self, data: str):
        print(data)
