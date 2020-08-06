class GuessHistory:
    def __init__(self):
        self.__history = []

    def add_guess(self, letter_or_word: str) -> None:
        self.__history.append(letter_or_word)

    def has_guess(self, letter_or_word: str) -> bool:
        return letter_or_word in self.__history

    def get_history(self) -> list:
        return self.__history


class GameHistory:
    def __init__(self):
        self.__history = []

    def add_game_result(self, is_game_won: bool) -> None:
        self.__history.append(is_game_won)

    def get_history(self) -> list:
        return self.__history

    def clear_history(self) -> None:
        self.__history.clear()
