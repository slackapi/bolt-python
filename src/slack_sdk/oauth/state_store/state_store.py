from abc import abstractmethod


class OAuthStateStore():
    def __init__(self):
        pass

    @abstractmethod
    def issue(self) -> str:
        NotImplementedError

    @abstractmethod
    def consume(self, state: str) -> bool:
        NotImplementedError
