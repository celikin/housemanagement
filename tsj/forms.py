# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Company, Resident, House, MeterReadingHistory, MeterType

class CompanyForm(ModelForm):
    username = forms.CharField(label=u"Имя пользователя", required=True)
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Company
        exclude = ('user',)


class AddHouseForm(forms.Form):
    house = forms.ChoiceField(label=u"Дома", choices=((house.id, house) for house in House.objects.all()),
        widget=forms.Select(attrs={'class': 'form-control'}))


class AddResidentForm(forms.Form):
    resident = forms.ChoiceField(label=u"Жилец", choices=((resident.id, resident) for resident in Resident.objects.all()),
        widget=forms.Select(attrs={'class': 'form-control'}))


class AddNotificationForm(forms.Form):
    notify = forms.IntegerField()


class NotifyForm(ModelForm):
    class Meta:
        exclude = ["pub_date"]
        model = Notification


class ResidentForm(ModelForm):
    username = forms.CharField(label='Имя пользователя', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label=u'Пароль', required=True)

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

class MeterForm(forms.ModelForm):
    meter_type = forms.ChoiceField(label=u"Тип счетчика", choices=((types.id, types) for types in MeterType.objects.all()),
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MeterReadingHistory
        fields = ('value',)
    
