#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
import datetime

class registerForm(forms.Form):
    Name = forms.CharField()
    Info = forms.CharField()
    def clean(self):
        cleaned_data = super(registerForm, self).clean()
        print(cleaned_data)
        return cleaned_data

class loginForm(forms.Form):
    Name = forms.CharField()
    Info = forms.CharField()

    def clean(self):
        cleaned_data = super(loginForm, self).clean()
        print(cleaned_data)
        return cleaned_data


class challengeForm(forms.Form):
    title = forms.CharField()
    detail = forms.CharField()
    award = forms.IntegerField(min_value=0)
    requirment = forms.CharField()


    def clean(self):
        cleaned_data = super(challengeForm, self).clean()
        return cleaned_data
