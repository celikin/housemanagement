# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Company, Resident


class CompanyForm(ModelForm):
    username = forms.CharField(label=u"Имя пользователя", required=True)
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Company


class ResidentForm(ModelForm):

    class Meta:
        model = Resident