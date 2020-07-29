import re
import random


class WordBank:
    """Stores a word list"""

    @classmethod
    def get_word_list(cls) -> list:
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed posuere justo orci, in mollis ex porta in. Pellentesque ullamcorper libero vel eros volutpat, sed sagittis ligula lacinia. Ut vel mollis metus. Aliquam quis nulla id eros tincidunt ultricies. Fusce sodales quis ante ut egestas. In tristique faucibus felis, sit amet."
        words = re.sub("\W", " ", text)

        return words.split()


class WordProvider:
    """Provides a word from a word Repository"""

    @classmethod
    def __filter_words(cls, word_list: list, by_word_length_range: tuple) -> list:

        return list(
            filter(
                lambda word: len(word)
                in range(by_word_length_range[0], by_word_length_range[1]),
                word_list,
            )
        )

    @classmethod
    def get_random_word(cls, filter_by_word_length_range: tuple) -> str:

        return random.choice(
            cls.__filter_words(WordBank.get_word_list(), filter_by_word_length_range)
        )
