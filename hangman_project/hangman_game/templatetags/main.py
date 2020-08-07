from django.template.defaulttags import register
from .. import forms


def get_dict_value(dictionary: dict, key):
    return dictionary.get(key)


@register.filter
def get_difficulty_title(difficulty_key):
    return get_dict_value(dict(forms.DIFFICULTY_CHOICES), difficulty_key)


@register.filter
def get_bool_to_win_loss(bool_key: bool):
    return {False: "Loss", True: "Win"}.get(bool_key)


@register.filter
def get_bool_list_to_win_loss(bool_keys: list):
    return [get_bool_to_win_loss(bool_key) for bool_key in bool_keys]
