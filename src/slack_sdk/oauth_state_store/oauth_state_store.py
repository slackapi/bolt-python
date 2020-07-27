class OAuthStateStore():
    def __init__(self):
        pass

    def issue(self) -> str:
        NotImplementedError

    def consume(self, state: str) -> bool:
        NotImplementedError