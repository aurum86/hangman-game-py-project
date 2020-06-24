import re
import random


def get_word_list() -> list:
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed posuere justo orci, in mollis ex porta in. Pellentesque ullamcorper libero vel eros volutpat, sed sagittis ligula lacinia. Ut vel mollis metus. Aliquam quis nulla id eros tincidunt ultricies. Fusce sodales quis ante ut egestas. In tristique faucibus felis, sit amet."
    words = re.sub("\W", " ", text)

    return words.split()


def get_random_word() -> str:

    return random.choice(get_word_list())
