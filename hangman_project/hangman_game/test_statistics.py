from django.test import TestCase
from unittest_data_provider import data_provider
from mock import MagicMock
from .statistics import *


class GuessHistoryTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__guess_history = GuessHistory()

    def test_add_guess(self):
        self.assertFalse(self.__guess_history.has_guess("a"))

        self.__guess_history.add_guess("a")

        self.assertTrue(self.__guess_history.has_guess("a"))

    def test_get_history(self):
        self.assertEqual([], self.__guess_history.get_history())

        self.__guess_history.add_guess("a")
        self.__guess_history.add_guess("0")

        self.assertEqual(["a", "0"], self.__guess_history.get_history())
