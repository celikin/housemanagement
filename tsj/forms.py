# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Company, Resident


class CompanyForm(ModelForm):
    username = forms.CharField(label=u"Имя пользователя")
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput())

    class Meta:
        model = Company
        exclude = ('user',)


class ResidentForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), label=u'Пароль', required=True)
    username = forms.CharField(label='Имя пользователя', required=True)

    
    class Meta:
        model = Resident
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'house',
            'flat',
            'bill_numb',
            'passport',
            'registration')
