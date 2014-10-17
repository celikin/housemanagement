# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Street(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название улицы')


class House(models.Model):
    number = models.CharField(max_length=4, verbose_name=u'Номер дома')


class Company(models.Model):
    TYPIES = (
        (0, u"ТСЖ"),
        (1, u"УК")
    )
    company_type = models.IntegerField(choices=TYPIES, default=0) 
    name = models.CharField(max_length=150)
    full_name = models.CharField(max_length=150)
    post_adress = models.TextField(verbose_name=u"Почтовый адрес")
    legal_adress = models.TextField(verbose_name=u"Юридический адрес")
    phone = models.CharField(max_length=15, verbose_name=u"Телефон")
    email = models.EmailField(verbose_name=u"E-mail")
    boss_fio = models.CharField(max_length=50, verbose_name=u"ФИО руководителя")
    inn = models.CharField(max_length=15, verbose_name=u"ИНН")
    orgn = models.CharField(max_length=15, verbose_name=u"ОРГН")
    orgn_date = models.CharField(max_length=15, verbose_name=u"Дата выдачи ОРГН")
    orgn_emitter = models.CharField(max_length=50, verbose_name=u"Кем выдан ОРГН")
    kpp = models.CharField(max_length=15, verbose_name=u"КПП")
    bill_numb = models.CharField(max_length=15, verbose_name=u"Расчетный счет")
    bank_name = models.CharField(max_length=150, verbose_name=u"В ОАО Банк")
    kor_schet = models.CharField(max_length=15, verbose_name=u"Кор. счет")
    bik = models.CharField(max_length=15, verbose_name=u"БИК")
    workgraph = models.TextField(verbose_name=u"График работы")


class Resident(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=15, verbose_name=u"Телефон")
    fio = models.CharField(max_length=100, verbose_name=u"ФИО")
    house = models.ForeignKey(House)
    flat = models.CharField(max_length=10)
    lnumb = models.CharField(max_length=20)
