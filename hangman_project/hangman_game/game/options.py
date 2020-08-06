from ..game import progress


class GameOptions:
    def __init__(
        self,
        difficulty: progress.Difficulty,
        translate_word: bool,
        target_language: str,
    ):
        self.__difficulty = difficulty
        self.__translate_word = translate_word
        self.__target_language = target_language

    @property
    def difficulty(self) -> progress.Difficulty:
        return self.__difficulty

    @property
    def translate_word(self) -> bool:
        return self.__translate_word

    @translate_word.setter
    def translate_word(self, value: bool) -> None:
        self.__translate_word = value

    @property
    def target_language(self) -> str:
        return self.__target_language

    @target_language.setter
    def target_language(self, value: str) -> None:
        self.__target_language = value
