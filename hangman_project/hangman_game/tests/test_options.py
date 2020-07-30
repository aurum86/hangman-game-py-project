from django.test import TestCase
from unittest_data_provider import data_provider
from ..game.options import *
import sys


class GameOptionsTest(TestCase):
    @data_provider(lambda: ((1, 1), (4, 2), (7, 3), (10, 4),))
    def test_get_word_length_min(
        self, expected_word_length, assumed_difficulty_level
    ) -> None:
        __game_options = GameOptions(difficulty_level=assumed_difficulty_level)

        self.assertEqual(expected_word_length, __game_options.get_word_length_min())

    @data_provider(lambda: ((3, 1), (6, 2), (9, 3), (sys.maxsize, 4),))
    def test_get_word_length_max(
        self, expected_word_length, assumed_difficulty_level
    ) -> None:
        __game_options = GameOptions(difficulty_level=assumed_difficulty_level)

        self.assertEqual(expected_word_length, __game_options.get_word_length_max())
