from django.test import TestCase
from unittest_data_provider import data_provider
from ..src.services import *


class GameStatusTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self._game_status = GameStatus()

    def test_property_status_default_value(self) -> None:
        self.assertIs(GameStatus.STATUS_BEGIN, self._game_status.status)

    def test_set_next(self) -> None:
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_1, self._game_status.status)
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_2, self._game_status.status)
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_3, self._game_status.status)
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_4, self._game_status.status)
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_5, self._game_status.status)
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_GAME_OVER, self._game_status.status)
        self._game_status.set_next()
        self.assertIs(GameStatus.STATUS_GAME_OVER, self._game_status.status)

    def test_reset(self) -> None:
        _game_status = GameStatus(GameStatus.STATUS_FAIL_5)
        _game_status.reset()

        self.assertIs(GameStatus.STATUS_BEGIN, self._game_status.status)

    @data_provider(lambda: (
            (False, GameStatus.STATUS_GAME_OVER),
            (True, GameStatus.STATUS_WIN),
    ))
    def test_finish_game(self, is_winner: bool, expected_status: GameStatus.STATUSES) -> None:
        self._game_status.finish_game(is_winner)

        self.assertIs(expected_status, self._game_status.status)


class SecretWordTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self._secret_word = SecretWord('somesecretword')

    @data_provider(lambda: (
            ('a', []),
            ('_', []),
            ('e', [3, 5, 8]),
    ))
    def test_get_letter_positions(self, letter, expected) -> None:
        self.assertListEqual(expected, self._secret_word.get_letter_positions(letter))

    def test_is_word(self) -> None:
        self.assertFalse(self._secret_word.is_word('some_incorrect_word'))
        self.assertTrue(self._secret_word.is_word('somesecretword'))

    def test_get_length(self) -> None:
        _secret_word = SecretWord('somesecretword')
        self.assertEqual(14, _secret_word.get_length())

        _secret_word = SecretWord('')
        self.assertEqual(0, _secret_word.get_length())

