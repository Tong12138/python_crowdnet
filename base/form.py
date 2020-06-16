#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
import datetime

class registerForm(forms.Form):
    Name = forms.CharField()
    Password = forms.CharField()
    Info = forms.CharField()
    def clean(self):
        cleaned_data = super(registerForm, self).clean()
        return cleaned_data

class loginForm(forms.Form):
    Name = forms.CharField()
    def clean(self):
        cleaned_data = super(loginForm, self).clean()
        return cleaned_data


class taskForm(forms.Form):
    title = forms.CharField()
    type = forms.CharField()
    detail = forms.CharField()
    award = forms.IntegerField(min_value=0)
    recievetime = forms.CharField()
    deadline = forms.CharField()
    requirment = forms.CharField()
    # data = forms.CharField()
    data = forms.FileField()
    flag = forms.CharField()
    public_key = forms.CharField()
    # flag = forms.CharField()

    def clean(self):
        cleaned_data = super(taskForm, self).clean()
        return cleaned_data

class profileForm(forms.Form):
    recharge = forms.CharField(required=False)
    skills = forms.CharField(required=False)
    def clean(self):
        cleaned_data = super(profileForm, self).clean()
        return cleaned_data

class commitForm(forms.Form):
    solution = forms.CharField()
    public_key = forms.CharField()
    def clean(self):
        cleaned_data = super(commitForm, self).clean()
        return cleaned_data

class rewardForm(forms.Form):
    workerid = forms.CharField()
    rate = forms.IntegerField(min_value=0, max_value=100)
    def clean(self):
        cleaned_data = super(rewardForm, self).clean()
        return cleaned_data
