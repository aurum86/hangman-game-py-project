from django.template.defaulttags import register
from .. import forms


def get_dict_value(dictionary: dict, key):
    return dictionary.get(key)


@register.filter
def get_difficulty_title(difficulty_key):
    return get_dict_value(dict(forms.DIFFICULTY_CHOICES), difficulty_key)
