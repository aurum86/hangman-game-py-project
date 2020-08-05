import sys


class Difficulty:
    DIFFICULTY_LEVEL_MIN = 1
    DIFFICULTY_LEVEL_MAX = 4

    def __init__(self, difficulty_level: int):
        self.difficulty_level = difficulty_level

    @property
    def difficulty_level(self) -> int:
        return self.__difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, value: int) -> None:
        if value not in range(self.DIFFICULTY_LEVEL_MIN, self.DIFFICULTY_LEVEL_MAX + 1):
            raise Exception("difficulty level ({}) is not valid".format(value))

        self.__difficulty_level = value

    def get_word_length_min(self) -> int:
        if self.difficulty_level == self.DIFFICULTY_LEVEL_MIN:
            return 1

        return Difficulty(self.difficulty_level - 1).get_word_length_max() + 1

    def get_word_length_max(self) -> int:
        if self.difficulty_level == self.DIFFICULTY_LEVEL_MAX:
            return sys.maxsize

        return self.get_word_length_min() + 2


class GameOptions:
    def __init__(
        self, difficulty: Difficulty, translate_word: bool, target_language: str
    ):
        self.__difficulty = difficulty
        self.__translate_word = translate_word
        self.__target_language = target_language

    @property
    def difficulty(self) -> Difficulty:
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
