from django import forms

DIFFICULTY_CHOICES = [(1, "Easy"), (2, "Normal"), (3, "Hard")]


class OptionsForm(forms.Form):
    difficulty_level = forms.ChoiceField(
        label='Select game difficulty',
        widget=forms.RadioSelect(attrs={
            # "class": "form-check-input",
        }),
        choices=DIFFICULTY_CHOICES,
    )