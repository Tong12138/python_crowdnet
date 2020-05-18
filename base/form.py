#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
import datetime

class registerForm(forms.Form):
    Name = forms.CharField()
    Password = forms.CharField()
    def clean(self):
        cleaned_data = super(registerForm, self).clean()
        return cleaned_data

class loginForm(forms.Form):
    Name = forms.CharField()
    Password = forms.CharField()
    Info = forms.CharField()


    def clean(self):
        cleaned_data = super(loginForm, self).clean()
        return cleaned_data


class challengeForm(forms.Form):
    title = forms.CharField()
    detail = forms.CharField()
    award = forms.IntegerField(min_value=0)
    requirment = forms.CharField()


    def clean(self):
        cleaned_data = super(challengeForm, self).clean()
        return cleaned_data

class profileForm(forms.Form):
    recharge = forms.CharField(required=False)
    skills = forms.CharField(required=False)
    def clean(self):
        cleaned_data = super(profileForm, self).clean()
        return cleaned_data

class commitForm(forms.Form):
    solution = forms.CharField()
    def clean(self):
        cleaned_data = super(commitForm, self).clean()
        return cleaned_data
