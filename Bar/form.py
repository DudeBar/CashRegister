# coding=utf-8

from django import forms


class OpenForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
