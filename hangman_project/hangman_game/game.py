from . import words
import collections


class GameStatus:
    """A class to determine game status"""

    STATUS_WIN = -1
    STATUS_BEGIN = 0
    STATUS_FAIL_1 = 1
    STATUS_FAIL_2 = 2
    STATUS_FAIL_3 = 3
    STATUS_FAIL_4 = 4
    STATUS_FAIL_5 = 5
    STATUS_FAIL_6 = 6
    STATUS_GAME_OVER = 7

    STATUSES = [
        STATUS_WIN,
        STATUS_BEGIN,
        STATUS_FAIL_1,
        STATUS_FAIL_2,
        STATUS_FAIL_3,
        STATUS_FAIL_4,
        STATUS_FAIL_5,
        STATUS_FAIL_6,
        STATUS_GAME_OVER,
    ]

    def __init__(self, initial_status: STATUSES = STATUS_BEGIN) -> None:
        self.__status = initial_status

    @property
    def status(self) -> STATUSES:
        return self.__status

    def set_next(self) -> None:
        current_index = self.STATUSES.index(self.status)
        if self.STATUS_GAME_OVER == self.status:
            return

        self.__status = self.STATUSES[current_index + 1]

    def reset(self) -> None:
        self.__status = self.STATUS_BEGIN

    def finish_game(self, is_winner: bool) -> None:
        if is_winner:
            self.__status = self.STATUS_WIN
        else:
            self.__status = self.STATUS_GAME_OVER


class SecretWord:
    """contains a secret word"""

    def __init__(self, secret_word: str) -> None:
        self.__secret_word = secret_word

    def get_letter_positions(self, letter: str) -> list:
        return [pos for pos, char in enumerate(self.__secret_word) if char == letter]

    def is_word(self, word: str) -> bool:
        return word == self.__secret_word

    def get_length(self) -> int:
        return len(self.__secret_word)

    def get_word(self) -> str:
        return self.__secret_word


class Hangman:
    """controls questions and punishment"""

    def __init__(self, secret_word: SecretWord, game_status: GameStatus) -> None:
        self.__secret_word = secret_word
        self.__game_status = game_status

    def ask_for_letter(self, letter: str) -> list:
        positions = self.__secret_word.get_letter_positions(letter)
        if not positions:
            self.__game_status.set_next()

            return []
        else:
            return positions

    def ask_for_word(self, word: str) -> bool:
        is_word = self.__secret_word.is_word(word)
        self.__game_status.finish_game(is_word)

        return is_word

    def get_game_status(self) -> GameStatus.STATUSES:
        return self.__game_status.status

    def is_game_finished(self) -> bool:
        return self.__game_status.status in [
            GameStatus.STATUS_WIN,
            GameStatus.STATUS_GAME_OVER,
        ]

    def get_word_length(self) -> int:
        return self.__secret_word.get_length()


class Knowledge:
    """stores what is revealed"""

    def __init__(self, hangman: Hangman):
        self.__hangman = hangman
        self.__known_letter_positions = collections.defaultdict(str)

    def get_all_letter_positions(self) -> dict:
        return self.__known_letter_positions

    def set_letters(self, letter: str, positions: list) -> None:
        if not positions:
            return

        for position in positions:
            self.__known_letter_positions[position] = letter

    def is_word_fully_revealed(self) -> bool:
        return len(self.get_all_letter_positions()) == self.__hangman.get_word_length()


class Convict:
    """Interacts with the Hangman based on the Knowledge possessed"""

    def __init__(self, hangman: Hangman, knowledge: Knowledge):
        self.__hangman = hangman
        self.__knowledge = knowledge

    def get_known_letter_positions(self) -> dict:
        return self.__knowledge.get_all_letter_positions()

    def get_game_status(self) -> GameStatus.STATUSES:
        return self.__hangman.get_game_status()

    def guess_word(self, word: str) -> bool:
        return self.__hangman.ask_for_word(word)

    def is_game_finished(self) -> bool:
        return self.__hangman.is_game_finished()

    def guess_letter(self, letter: str) -> bool:
        __positions = self.__hangman.ask_for_letter(letter)
        self.__knowledge.set_letters(letter, __positions)

        if self.__knowledge.is_word_fully_revealed():
            return self.__hangman.ask_for_word(self.__get_known_word())

        return len(__positions) > 0

    def __get_known_word(self) -> str:
        __positions = self.__knowledge.get_all_letter_positions()

        return "".join(dict(sorted(__positions.items())).values())


class ConvictFactory:
    @classmethod
    def create_convict(cls, secret_word: SecretWord) -> Convict:
        __game_status = GameStatus(GameStatus.STATUS_BEGIN)
        __hangman = Hangman(secret_word=secret_word, game_status=__game_status)
        __knowledge = Knowledge(hangman=__hangman)

        return Convict(hangman=__hangman, knowledge=__knowledge)


class SecretWordFactory:
    def __init__(self, word_provider: words.WordProvider):
        self.__word_provider = word_provider

    def create_secret_word(self, word_length_range: tuple):
        __random_word = self.__word_provider.get_random_word(word_length_range).lower()

        return SecretWord(secret_word=__random_word)
