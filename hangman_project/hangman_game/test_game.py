from django.test import TestCase
from unittest_data_provider import data_provider
from mock import MagicMock
from .game import *


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
        self.assertIs(GameStatus.STATUS_FAIL_6, self._game_status.status)
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


class HangmanTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self._mock_secret_word = MagicMock(spec=SecretWord)
        self._mock_game_status = MagicMock(spec=GameStatus)

        self._hangman = Hangman(self._mock_secret_word, self._mock_game_status)

    def test_ask_for_letter_when_letter_is_correct(self) -> None:

        self._mock_secret_word.get_letter_positions.return_value = [2, 5]

        result = self._hangman.ask_for_letter('a')

        self.assertEqual([2, 5], result)
        self._mock_secret_word.get_letter_positions.assert_called_once_with('a')

    def test_ask_for_letter_when_letter_is_not_correct(self) -> None:
        _hangman = Hangman(self._mock_secret_word, self._mock_game_status)

        self._mock_secret_word.get_letter_positions.return_value = []

        result = self._hangman.ask_for_letter('a')

        self.assertEqual([], result)
        self._mock_secret_word.get_letter_positions.assert_called_once_with('a')
        self._mock_game_status.set_next.assert_called_once()

    @data_provider(lambda: (
            ('word is correct', True),
            ('word is not correct', False),
    ))
    def test_ask_for_word(self, case, expect_is_word: bool) -> None:
        self._mock_secret_word.is_word.return_value = expect_is_word

        result = self._hangman.ask_for_word('someword')

        self.assertEqual(expect_is_word, result)
        self._mock_secret_word.is_word.assert_called_with('someword')
        self._mock_game_status.finish_game.assert_called_with(expect_is_word)

    def test_get_game_status(self) -> None:
        self._mock_game_status.status = GameStatus.STATUS_FAIL_4

        self.assertEqual(GameStatus.STATUS_FAIL_4, self._hangman.get_game_status())

        self._mock_game_status.status = GameStatus.STATUS_GAME_OVER

        self.assertEqual(GameStatus.STATUS_GAME_OVER, self._hangman.get_game_status())

    @data_provider(lambda: (
            (False, GameStatus.STATUS_FAIL_4),
            (False, GameStatus.STATUS_BEGIN),
            (True, GameStatus.STATUS_WIN),
            (True, GameStatus.STATUS_GAME_OVER),
    ))
    def test_get_game_status(self, expected_game_finished: bool, game_status: GameStatus.STATUSES) -> None:
        self._mock_game_status.status = game_status

        self.assertEqual(expected_game_finished, self._hangman.is_game_finished())

    def test_get_word_length(self):
        self._mock_secret_word.get_length.return_value = 5

        self.assertEqual(5, self._hangman.get_word_length())

        self._mock_secret_word.get_length.return_value = 0

        self.assertEqual(0, self._hangman.get_word_length())

