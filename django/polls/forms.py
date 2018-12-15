from django import forms

class ChoicesForm(forms.Form):
    choice = forms.ChoiceField(choices=(),required=False,widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = self.initial['choices']