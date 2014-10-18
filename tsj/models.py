# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator

class Street(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название улицы')


class House(models.Model):
    street = models.ForeignKey(Street)
    number = models.CharField(max_length=4, verbose_name=u'Номер дома')

    def __unicode__(self):
        return '%s, %s' % (self.street.name, self.number)


class BaseCompany(models.Model):
    name = models.CharField(max_length=150, verbose_name=u"Название")
    full_name = models.CharField(max_length=150, verbose_name=u"Полное наимаенование")
    post_address = models.TextField(verbose_name=u"Почтовый адрес")
    legal_address = models.TextField(verbose_name=u"Юридический адрес")
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

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Company(BaseCompany):
    TYPIES = (
        (0, u"ТСЖ"),
        (1, u"УК")
    )
    user = models.OneToOneField(User)
    houses = models.ManyToManyField(House)
    company_type = models.IntegerField(choices=TYPIES, default=0, verbose_name=u"Тип")
    proof = models.FileField(upload_to="scans", verbose_name=u"Подтверждающий документ")
    services = models.ManyToManyField("ServiceCompany", related_name="%(app_label)s_%(class)s_related")

    def get_residents(self):
        return Resident.objects.filter(house__id__in=self.houses.all())


class ServiceCompany(BaseCompany):
    pass


class Resident(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=15, verbose_name=u"Телефон")
    first_name = models.CharField(max_length=150, verbose_name=u"Имя")
    last_name = models.CharField(max_length=150, verbose_name=u"Фамилия")
    middle_name = models.CharField(max_length=150, verbose_name=u"Отчество")
    house = models.ForeignKey(House, verbose_name=u"Улица")
    flat = models.CharField(max_length=10, verbose_name=u"Номер квартиры")
    bill_numb = models.CharField(max_length=20, verbose_name=u"Номер лицевого счёта")
    passport = models.FileField(upload_to="scans", verbose_name=u"Скан паспорта")
    registration = models.FileField(upload_to="scans", verbose_name=u"Скан прописки")

    def __unicode__(self):
        return u"%s %s (%s, кв. %s)" % (self.first_name, self.last_name, self.house, self.flat)


class MeterType(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"Название")
    measurment = models.CharField(max_length=20, verbose_name=u"Измеряется в")

    def __unicode__(self):
        return self.name


class Employer(models.Model):
    phone = models.CharField(max_length=15, verbose_name=u"Телефон")
    first_name = models.CharField(max_length=150, verbose_name=u"Имя")
    last_name = models.CharField(max_length=150, verbose_name=u"Фамилия")
    middle_name = models.CharField(max_length=150, verbose_name=u"Отчество")
    profession = models.CharField(max_length=100, verbose_name=u"Профессия")
<<<<<<< HEAD
    company = models.ForeignKey(Company, verbose_name=u"Компания")
=======
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.profession + ' ' + self.first_name
>>>>>>> 864847e2c407276bdb653213772e2f0ad3682912

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class MeterReadingHistory(models.Model):
    resident = models.ForeignKey(Resident)
    value = models.IntegerField(verbose_name=u"Значение",
        validators=[
            MinValueValidator(1)
        ])
    adding_date = models.DateField(default=datetime.now, verbose_name=u"Дата снятия показаний")
    meter_type = models.ForeignKey(MeterType)

    def __unicode__(self):
        return u"%s - %s" % (self.resident.last_name, self.value)


class Notification(models.Model):
    NOTIFICATIONS = (
        (0, u"Отключение воды"),
        (1, u"Отключение света"),
        (2, u"Собрание"),
        (3, u"Общее"),
    )
    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата публикации')
    text = models.TextField(verbose_name=u"Текст")
    note_type = models.IntegerField(choices=NOTIFICATIONS, default=3, verbose_name=u"Тип")
    houses = models.ManyToManyField(House)
