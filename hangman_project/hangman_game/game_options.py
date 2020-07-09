import sys


class GameOptions:
    DIFFICULTY_LEVEL_MIN = 1
    DIFFICULTY_LEVEL_MAX = 4

    def __init__(self, difficulty_level: int):
        self.difficulty_level = difficulty_level

    @property
    def difficulty_level(self) -> int:
        return self._difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, value) -> None:
        if value not in range(self.DIFFICULTY_LEVEL_MIN, self.DIFFICULTY_LEVEL_MAX + 1):
            raise Exception("difficulty level ({}) is not valid".format(value))

        self._difficulty_level = value

    def get_word_length_min(self) -> int:
        if self.difficulty_level == self.DIFFICULTY_LEVEL_MIN:
            return 1

        return GameOptions(self.difficulty_level - 1).get_word_length_max() + 1

    def get_word_length_max(self) -> int:
        if self.difficulty_level == self.DIFFICULTY_LEVEL_MAX:
            return sys.maxsize

        return self.get_word_length_min() + 2
