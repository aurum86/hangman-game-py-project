
class GameStatus:
    """A class to determine game status"""
    STATUS_WIN = -1
    STATUS_BEGIN = 0
    STATUS_FAIL_1 = 1
    STATUS_FAIL_2 = 2
    STATUS_FAIL_3 = 3
    STATUS_FAIL_4 = 4
    STATUS_FAIL_5 = 5
    STATUS_GAME_OVER = 6

    STATUSES = [
        STATUS_WIN,
        STATUS_BEGIN,
        STATUS_FAIL_1,
        STATUS_FAIL_2,
        STATUS_FAIL_3,
        STATUS_FAIL_4,
        STATUS_FAIL_5,
        STATUS_GAME_OVER
    ]

    def __init__(self, initial_status: STATUSES = STATUS_BEGIN):
        self._status = initial_status

    @property
    def status(self) -> STATUSES:
        return self._status

    def set_next(self):
        current_index = self.STATUSES.index(self.status)
        if self.STATUS_GAME_OVER == self.status:
            return

        self._status = self.STATUSES[current_index + 1]

    def reset(self):
        self._status = self.STATUS_BEGIN

    def finish_game(self, is_winner: bool):
        if is_winner:
            self._status = self.STATUS_WIN
        else:
            self._status = self.STATUS_GAME_OVER


class SecretWord:
    """contains a secret word"""

    def __init__(self, secret_word: str):
        self._secret_word = secret_word

    def get_letter_positions(self, letter: str) -> list:
        return [pos for pos, char in enumerate(self._secret_word) if char == letter]

    def is_word(self, word: str) -> bool:
        return word == self._secret_word

    def get_length(self) -> int:
        return len(self._secret_word)


class Knowledge:
    """stores what is revealed"""

    _UNKNOWN_CHAR = '*'

    def __init__(self, word_length: int):
        self._word_length = word_length
        self._word = None

    def get_word(self, unknown_char_shown_as: str = _UNKNOWN_CHAR):
        if self._word is None:
            return unknown_char_shown_as * self._word_length
        else:
            return self._word


class Hangman:
    """defines a way to guess"""

    def __init__(self,
                 secret_word: SecretWord,
                 game_status: GameStatus
                 ):
        self._secret_word = secret_word
        self._game_status = game_status

    def ask_for_letter(self, letter: str):
        positions = self._secret_word.get_letter_positions(letter)
        if not positions:
            self._game_status.set_next()

    def ask_for_word(self, word: str):
        self._game_status.finish_game(self._secret_word.is_word(word))

    def get_game_status(self) -> GameStatus.STATUSES:
        return self._game_status.status
