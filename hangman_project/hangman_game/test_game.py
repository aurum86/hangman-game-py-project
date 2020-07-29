from django.test import TestCase
from unittest_data_provider import data_provider
from mock import MagicMock
from .game import *


class GameStatusTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__game_status = GameStatus()

    def test_property_status_default_value(self) -> None:
        self.assertIs(GameStatus.STATUS_BEGIN, self.__game_status.status)

    def test_set_next(self) -> None:
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_1, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_2, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_3, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_4, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_5, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_FAIL_6, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_GAME_OVER, self.__game_status.status)
        self.__game_status.set_next()
        self.assertIs(GameStatus.STATUS_GAME_OVER, self.__game_status.status)

    def test_reset(self) -> None:
        __game_status = GameStatus(GameStatus.STATUS_FAIL_5)
        __game_status.reset()

        self.assertIs(GameStatus.STATUS_BEGIN, self.__game_status.status)

    @data_provider(
        lambda: ((False, GameStatus.STATUS_GAME_OVER), (True, GameStatus.STATUS_WIN),)
    )
    def test_finish_game(
        self, is_winner: bool, expected_status: GameStatus.STATUSES
    ) -> None:
        self.__game_status.finish_game(is_winner)

        self.assertIs(expected_status, self.__game_status.status)


class SecretWordTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__secret_word = SecretWord("somesecretword")

    @data_provider(lambda: (("a", []), ("_", []), ("e", [3, 5, 8]),))
    def test_get_letter_positions(self, letter, expected) -> None:
        self.assertListEqual(expected, self.__secret_word.get_letter_positions(letter))

    def test_is_word(self) -> None:
        self.assertFalse(self.__secret_word.is_word("some_incorrect_word"))
        self.assertTrue(self.__secret_word.is_word("somesecretword"))

    def test_get_length(self) -> None:
        __secret_word = SecretWord("somesecretword")
        self.assertEqual(14, __secret_word.get_length())

        __secret_word = SecretWord("")
        self.assertEqual(0, __secret_word.get_length())


class HangmanTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__mock_secret_word = MagicMock(spec=SecretWord)
        self.__mock_game_status = MagicMock(spec=GameStatus)

        self.__hangman = Hangman(self.__mock_secret_word, self.__mock_game_status)

    def test_ask_for_letter_when_letter_is_correct(self) -> None:

        self.__mock_secret_word.get_letter_positions.return_value = [2, 5]

        result = self.__hangman.ask_for_letter("a")

        self.assertEqual([2, 5], result)
        self.__mock_secret_word.get_letter_positions.assert_called_once_with("a")

    def test_ask_for_letter_when_letter_is_not_correct(self) -> None:
        __hangman = Hangman(self.__mock_secret_word, self.__mock_game_status)

        self.__mock_secret_word.get_letter_positions.return_value = []

        result = self.__hangman.ask_for_letter("a")

        self.assertEqual([], result)
        self.__mock_secret_word.get_letter_positions.assert_called_once_with("a")
        self.__mock_game_status.set_next.assert_called_once()

    @data_provider(lambda: (("word is correct", True), ("word is not correct", False),))
    def test_ask_for_word(self, case, expect_is_word: bool) -> None:
        self.__mock_secret_word.is_word.return_value = expect_is_word

        result = self.__hangman.ask_for_word("someword")

        self.assertEqual(expect_is_word, result)
        self.__mock_secret_word.is_word.assert_called_with("someword")
        self.__mock_game_status.finish_game.assert_called_with(expect_is_word)

    def test_get_game_status(self) -> None:
        self.__mock_game_status.status = GameStatus.STATUS_FAIL_4

        self.assertEqual(GameStatus.STATUS_FAIL_4, self.__hangman.get_game_status())

        self.__mock_game_status.status = GameStatus.STATUS_GAME_OVER

        self.assertEqual(GameStatus.STATUS_GAME_OVER, self.__hangman.get_game_status())

    @data_provider(
        lambda: (
            (False, GameStatus.STATUS_FAIL_4),
            (False, GameStatus.STATUS_BEGIN),
            (True, GameStatus.STATUS_WIN),
            (True, GameStatus.STATUS_GAME_OVER),
        )
    )
    def test_get_game_status(
        self, expected_game_finished: bool, game_status: GameStatus.STATUSES
    ) -> None:
        self.__mock_game_status.status = game_status

        self.assertEqual(expected_game_finished, self.__hangman.is_game_finished())

    def test_get_word_length(self) -> None:
        self.__mock_secret_word.get_length.return_value = 5

        self.assertEqual(5, self.__hangman.get_word_length())

        self.__mock_secret_word.get_length.return_value = 0

        self.assertEqual(0, self.__hangman.get_word_length())


class KnowledgeTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__mock_hangman = MagicMock(spec=Hangman)

    def test_get_letter_positions(self):

        self.assertEqual({}, Knowledge(self.__mock_hangman).get_all_letter_positions())

    def test_set_letters(self):
        __knowledge = Knowledge(self.__mock_hangman)

        __knowledge.set_letters("s", [])
        self.assertEqual({}, __knowledge.get_all_letter_positions())

        __knowledge.set_letters("s", [2, 4])
        self.assertEqual({2: "s", 4: "s"}, __knowledge.get_all_letter_positions())

        __knowledge.set_letters("a", [1, 6])
        self.assertEqual(
            {1: "a", 2: "s", 4: "s", 6: "a"}, __knowledge.get_all_letter_positions()
        )

    @data_provider(
        lambda: (
            (False, {2: "s"}, 0),
            (False, {}, 1),
            (True, {1: "a"}, 1),
            (True, {}, 0),
        )
    )
    def test_is_word_fully_revealed(
        self, expected: bool, known_letters, word_length
    ) -> None:
        __knowledge = Knowledge(self.__mock_hangman)

        self.__mock_hangman.get_word_length.return_value = word_length
        items = list(known_letters.items())
        if items:
            __knowledge.set_letters(letter=items[0][1], positions=[items[0][0]])

        self.assertEqual(expected, __knowledge.is_word_fully_revealed())


class ConvictTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__mock_hangman = MagicMock(spec=Hangman)
        self.__mock_knowledge = MagicMock(spec=Knowledge)
        self.__convict = Convict(
            hangman=self.__mock_hangman, knowledge=self.__mock_knowledge
        )

    def test_get_known_letter_positions(self) -> None:
        __expected = {1: "t", 2: "e"}
        self.__mock_knowledge.get_all_letter_positions.return_value = __expected

        self.assertEqual(__expected, self.__convict.get_known_letter_positions())

    def test_get_game_status(self) -> None:
        self.__mock_hangman.get_game_status.return_value = GameStatus.STATUS_FAIL_4

        self.assertEqual(GameStatus.STATUS_FAIL_4, self.__convict.get_game_status())

    def test_guess_word(self) -> None:
        self.__mock_hangman.ask_for_word.return_value = True

        self.assertTrue(self.__convict.guess_word("someword"))

    def test_is_game_finished(self) -> None:
        self.__mock_hangman.is_game_finished.return_value = True

        self.assertTrue(self.__convict.is_game_finished())

    @data_provider(
        lambda: (
            (False, [], False, False),
            (True, [1], False, False),
            (True, [1], True, True),
            (True, [], True, True),
        )
    )
    def test_guess_letter(
        self,
        expected_is_correct: bool,
        assume_letter_positions: list,
        assume_is_word_fully_revealed: bool,
        expect_ask_for_word_is_called: bool,
    ) -> None:
        self.__mock_hangman.ask_for_letter.return_value = assume_letter_positions
        self.__mock_hangman.ask_for_word.return_value = True

        self.__mock_knowledge.is_word_fully_revealed.return_value = (
            assume_is_word_fully_revealed
        )
        self.__mock_knowledge.get_all_letter_positions.return_value = {
            1: "t",
            2: "e",
            3: "s",
            4: "t",
        }

        self.assertEqual(expected_is_correct, self.__convict.guess_letter("s"))

        self.__mock_knowledge.set_letters.assert_called_with(
            "s", assume_letter_positions
        )
        if expect_ask_for_word_is_called:
            self.__mock_hangman.ask_for_word.assert_called_with("test")
        else:
            self.__mock_hangman.ask_for_word.assert_not_called()
