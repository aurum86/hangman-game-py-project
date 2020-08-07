from django.test import TestCase
from unittest_data_provider import data_provider
from mock import MagicMock
from ..game.progress import *
from ..game.statistics import *
import sys


class DifficultyTest(TestCase):
    @data_provider(lambda: ((1, 1), (4, 2), (7, 3), (10, 4),))
    def test_get_word_length_min(
        self, expected_word_length, assumed_difficulty_level
    ) -> None:
        __game_options = Difficulty(difficulty_level=assumed_difficulty_level, level_min=1, level_max=4)

        self.assertEqual(expected_word_length, __game_options.get_word_length_min())

    @data_provider(lambda: ((3, 1), (6, 2), (9, 3), (sys.maxsize, 4),))
    def test_get_word_length_max(
        self, expected_word_length, assumed_difficulty_level
    ) -> None:
        __game_options = Difficulty(difficulty_level=assumed_difficulty_level, level_min=1, level_max=4)

        self.assertEqual(expected_word_length, __game_options.get_word_length_max())


class ProgressEvaluatorTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__mock_game_history = MagicMock(spec=GameHistory)
        self.__progress_evaluator = ProgressEvaluator(
            game_history=self.__mock_game_history
        )

    @data_provider(
        lambda: (
            (-1, [False, False]),
            (-1, [True, False, False]),
            (-1, [True, True, True, True, False, False]),
            (0, [True]),
            (0, [True, True]),
            (0, [False]),
            (0, [True, False]),
            (0, [True, True, False]),
            (0, [False, True]),
            (0, [True, True, True, False, True]),
            (1, [True, True, True]),
            (1, [False, True, True, True]),
            (1, [False, False, False, False, True, True, True]),
        )
    )
    def test_evaluate_game_level(self, expected: int, assumed_history: list) -> None:
        self.__mock_game_history.get_history.return_value = assumed_history

        self.assertEqual(
            expected, self.__progress_evaluator.get_next_level_evaluation()
        )
