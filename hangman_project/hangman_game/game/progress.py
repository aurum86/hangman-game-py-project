import sys
from . import statistics


class Difficulty:
    def __init__(self, difficulty_level: int, level_min: int, level_max: int):
        self.__level_min = level_min
        self.__level_max = level_max
        self.difficulty_level = difficulty_level

    @property
    def difficulty_level(self) -> int:
        return self.__difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, value: int) -> None:
        if value not in range(
            self.__level_min, self.__level_max + 1
        ):
            raise Exception("difficulty level ({}) is not valid".format(value))

        self.__difficulty_level = value

    def get_word_length_min(self) -> int:
        if self.difficulty_level == self.__level_min:
            return 1

        return DifficultyFactory.create_difficulty(self.difficulty_level - 1).get_word_length_max() + 1

    def get_word_length_max(self) -> int:
        if self.difficulty_level == self.__level_max:
            return sys.maxsize

        return self.get_word_length_min() + 2


class ProgressEvaluator:
    __MIN_WINS_TO_NEXT_LEVEL = 3
    __MIN_LOSSES_TO_PREV_LEVEL = 2

    def __init__(self, game_history: statistics.GameHistory):
        self.__game_history = game_history

    def get_last_wins_and_loses(self) -> list:
        return self.__game_history.get_history()[-3:]

    def get_next_level_evaluation(self) -> int:
        __last_results = self.get_last_wins_and_loses()

        if len(__last_results) < 2:
            return 0

        if __last_results.count(True) == self.__MIN_WINS_TO_NEXT_LEVEL:
            return 1
        if __last_results.count(False) >= self.__MIN_LOSSES_TO_PREV_LEVEL:
            return -1

        return 0


class Progress:
    def __init__(
        self,
        progress_evaluator: ProgressEvaluator,
        game_history: statistics.GameHistory,
        current_level: int,
    ):
        self.__progress_evaluator = progress_evaluator
        self.__game_history = game_history
        self.__current_level = current_level

    def __filter_game_level(self):
        if self.__current_level < 1:
            self.__current_level = 1

        if self.__current_level > 3:
            self.__current_level = 3

    def evaluate_game_level(self) -> None:
        __evaluation = self.__progress_evaluator.get_next_level_evaluation()

        if abs(__evaluation) > 0:
            self.__game_history.clear_history()
            self.__current_level += __evaluation
            self.__filter_game_level()

    def get_game_level(self) -> int:
        return self.__current_level

    def get_last_wins_and_loses(self) -> list:
        return self.__game_history.get_history()[-3:]

    @property
    def game_history(self) -> statistics.GameHistory:
        return self.__game_history


class DifficultyFactory:
    @classmethod
    def create_difficulty(cls, difficulty_level: int) -> Difficulty:
        return Difficulty(difficulty_level=difficulty_level, level_min=1, level_max=4)


class ProgressFactory:
    @classmethod
    def create_progress(cls, level: int) -> Progress:
        __game_history = statistics.GameHistory()
        __progress_evaluator = ProgressEvaluator(__game_history)
        return Progress(
            progress_evaluator=__progress_evaluator,
            game_history=__game_history,
            current_level=level,
        )
