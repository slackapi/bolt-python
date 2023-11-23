import abc


class Protocol(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "name")
            and hasattr(subclass, "debug")
            and callable(subclass.debug)
            and hasattr(subclass, "info")
            and callable(subclass.info)
            and hasattr(subclass, "warning")
            and callable(subclass.warning)
            and hasattr(subclass, "error")
            and callable(subclass.error)
            and hasattr(subclass, "respond")
            and callable(subclass.respond)
        )

    @abc.abstractmethod
    def debug(self, msg: str, *args, **kwargs):
        """Logs a message with level DEBUG"""
        raise NotImplementedError

    @abc.abstractmethod
    def info(self, msg: str, *args, **kwargs):
        """Logs a message with level INFO"""
        raise NotImplementedError

    @abc.abstractmethod
    def warning(self, msg: str, *args, **kwargs):
        """Logs a message with level WARNING"""
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, msg: str, *args, **kwargs):
        """Logs a message with level ERROR on the root logger"""
        raise NotImplementedError

    @abc.abstractmethod
    def respond(self, data: str):
        """Utility method for responding to CLI hook invocations"""
        raise NotImplementedError
