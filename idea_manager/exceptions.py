class NotFoundIdeaError(Exception):
    def __init__(self, text: str) -> None:
        self.text = text
