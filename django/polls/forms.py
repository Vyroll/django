from django import forms

from .models import Question

class ChoicesForm(forms.Form):
    choice = forms.ChoiceField(choices=(),required=False,widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Question.objects.get(pk=self.initial['pk']).choice_set.all()
        choices = tuple((choice.id,choice.choice_text) for choice in choices)
        self.fields['choice'].choices = choices

class createPersonForm(forms.Form):
    person = forms.CharField(max_length=50, required=True)
    task = forms.CharField(max_length=50, required=True)