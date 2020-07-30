from django.test import TestCase
from unittest_data_provider import data_provider
from mock import MagicMock

from ..views.game import KnownWordPrinter
from ..game import game


class KnownWordPrinterTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__mock_convict = MagicMock(spec=game.Convict)
        self.__mock_secret_word = MagicMock(spec=game.SecretWord)

        self.__known_word_printer = KnownWordPrinter(
            self.__mock_convict, self.__mock_secret_word
        )

    @data_provider(
        lambda: (
            ("", {}, 0),
            ("", {2: "s"}, 0),
            ("**", {}, 2),
            ("t*st", {0: "t", 2: "s", 3: "t"}, 4),
        )
    )
    def test_get_known_word(
        self, expected: str, known_letters: dict, word_length: int
    ) -> None:
        self.__mock_convict.get_known_letter_positions.return_value = known_letters
        self.__mock_secret_word.get_length.return_value = word_length

        self.assertEqual(
            expected, self.__known_word_printer.get_known_word(),
        )
