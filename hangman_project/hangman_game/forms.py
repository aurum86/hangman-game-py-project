from django import forms

DIFFICULTY_CHOICES = [(1, "Easy"), (2, "Normal"), (3, "Hard")]


class OptionsForm(forms.Form):

    difficulty_level = forms.ChoiceField(
        label="Select game initial difficulty",
        widget=forms.RadioSelect(),
        choices=DIFFICULTY_CHOICES,
    )
    translate_word = forms.BooleanField(
        label="Translate the word in the end of the game.",
        widget=forms.CheckboxInput(),
        required=False,
    )

    __TARGET_LANGUAGES = [
        ("lt", "Lithuanian"),
        ("en", "English"),
        ("de", "German"),
        ("ru", "Russian"),
    ]

    target_language = forms.ChoiceField(
        label="Select target language for translation",
        widget=forms.RadioSelect(),
        choices=__TARGET_LANGUAGES,
    )
