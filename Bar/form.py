# coding=utf-8

from django import forms


class OpenForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class NoteForm(forms.Form):
    CHOICES = ((1,"Normal"), (2,"Important"))
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial=1)