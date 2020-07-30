class OAuthStateStore():
    def __init__(self):
        pass

    def issue(self) -> str:
        pass

    def consume(self, state: str) -> bool:
        pass
