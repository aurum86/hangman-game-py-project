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
        self._status = initial_status

    @property
    def status(self) -> STATUSES:
        return self._status

    def set_next(self) -> None:
        current_index = self.STATUSES.index(self.status)
        if self.STATUS_GAME_OVER == self.status:
            return

        self._status = self.STATUSES[current_index + 1]

    def reset(self) -> None:
        self._status = self.STATUS_BEGIN

    def finish_game(self, is_winner: bool) -> None:
        if is_winner:
            self._status = self.STATUS_WIN
        else:
            self._status = self.STATUS_GAME_OVER


class SecretWord:
    """contains a secret word"""

    def __init__(self, secret_word: str) -> None:
        self._secret_word = secret_word

    def get_letter_positions(self, letter: str) -> list:
        return [pos for pos, char in enumerate(self._secret_word) if char == letter]

    def is_word(self, word: str) -> bool:
        return word == self._secret_word

    def get_length(self) -> int:
        return len(self._secret_word)

    def get_word(self) -> str:
        return self._secret_word


class Hangman:
    """controls questions and punishment"""

    def __init__(self, secret_word: SecretWord, game_status: GameStatus) -> None:
        self._secret_word = secret_word
        self._game_status = game_status

    def ask_for_letter(self, letter: str) -> list:
        positions = self._secret_word.get_letter_positions(letter)
        if not positions:
            self._game_status.set_next()

            return []
        else:
            return positions

    def ask_for_word(self, word: str) -> bool:
        is_word = self._secret_word.is_word(word)
        self._game_status.finish_game(is_word)

        return is_word

    def get_game_status(self) -> GameStatus.STATUSES:
        return self._game_status.status

    def is_game_finished(self) -> bool:
        return self._game_status.status in [
            GameStatus.STATUS_WIN,
            GameStatus.STATUS_GAME_OVER,
        ]

    def get_word_length(self) -> int:
        return self._secret_word.get_length()


class Knowledge:
    """stores what is revealed"""

    _UNKNOWN_CHAR = "*"

    def __init__(self, hangman: Hangman, known_word: str = None):
        self._hangman = hangman
        self._known_word = known_word

    # TODO: this parameter "unknown_char_shown_as" should be removed from here
    def get_word(self, unknown_char_shown_as: str = _UNKNOWN_CHAR) -> str:
        if self._known_word is None:
            return unknown_char_shown_as * self._hangman.get_word_length()
        else:
            return self._known_word

    def set_letters(self, positions: list, letter: str) -> None:
        if not positions:
            return

        self._known_word = "".join(
            [
                letter if i in positions else char
                for i, char in enumerate(self.get_word())
            ]
        )

    def is_word_fully_revealed(self) -> bool:
        return self._known_word.count(self._UNKNOWN_CHAR) == 0


class Convict:
    """Interacts with the Hangman based on the Knowledge possessed"""

    def __init__(self, hangman: Hangman, knowledge: Knowledge):
        self._hangman = hangman
        self._knowledge = knowledge

    def get_known_word(self) -> str:
        return self._knowledge.get_word()

    def get_game_status(self) -> GameStatus.STATUSES:
        return self._hangman.get_game_status()

    def guess_word(self, word: str) -> bool:
        return self._hangman.ask_for_word(word)

    def is_game_finished(self) -> bool:
        return self._hangman.is_game_finished()

    def guess_letter(self, letter: str) -> bool:
        _positions = self._hangman.ask_for_letter(letter)
        self._knowledge.set_letters(_positions, letter)

        if self._knowledge.is_word_fully_revealed():
            return self._hangman.ask_for_word(self._knowledge.get_word())

        return len(_positions) > 0


class ConvictFactory:
    @classmethod
    def create_convict(cls, secret_word: SecretWord) -> Convict:
        _game_status = GameStatus(GameStatus.STATUS_BEGIN)
        _hangman = Hangman(secret_word=secret_word, game_status=_game_status)
        _knowledge = Knowledge(hangman=_hangman, known_word=None)

        return Convict(
            hangman=_hangman,
            knowledge=_knowledge
        )


class SecretWordFactory:
    def __init__(self, words):
        self._words = words

    def create_secret_word(self, word_length_range: tuple):
        _random_word = self._words.get_random_word(word_length_range).lower()

        return SecretWord(secret_word=_random_word)
