
class Player():
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def get_name(self) -> str:
        return self.name

    def get_score(self) -> int:
        return self.score

    def killed_invader(self) -> None:
        self.add_to_score(50)

    def add_to_score(self, adder: int) -> None:
        self.score += adder