# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CompanyForm, ResidentForm, AddHouseForm, AddResidentForm, NotifyForm, AddNotificationForm
from .models import Resident, Company, House, Notification
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.forms.models import model_to_dict


def is_org(user):
    if not user.is_authenticated():
        return False
    try:
        user = Resident.objects.get(user=user)
    except Resident.DoesNotExist:
        return True
    return False


def home(request):
    if not request.user.is_authenticated():
        return render(request, "home.html")
    if is_org(request.user):
        return redirect(reverse("orghome"))
    return render(request, "user/home.html")


def orghome(request):
    if not request.user.is_authenticated() or not is_org(request.user):
        return redirect(reverse("home"))

    if not is_org(request.user):
        return redirect(reverse("home"))
    return render(request, "org/home.html")


def auth(request):
    if request.method != "POST":
        return redirect(reverse("home"))

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(reverse("home"))
    else:
        messages.error(request, 'К сожалению, вы ввели неправильный логин или пароль')
        return redirect(reverse("home"))


def registration(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))

    form = ResidentForm()
    return render(request, "user/registration.html", {
        "form": form
    })


def common_registration(request, Form, template):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == "POST":
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.save()
            entity = form.save(commit=False)
            entity.user = user
            messages.success(request, 'Вы успешно зарегестрированы. Ожидайте подтверждения')
            entity.save()
            return redirect(reverse('home'))
    else:
        form = Form()
    return render(request, template, {
        "form": form
    })


def orgregistration(request):
    return common_registration(request, CompanyForm, 'org/registration.html')


def orgprofile(request):
    if not is_org(request.user):
        return redirect(reverse("userprofile"))
    profile = CompanyForm(data=model_to_dict(Company.objects.get(user=request.user)))
    return render(request, "org/profile.html", {
        "profile": profile,
    })


def view_notification(request):
    pass


def create_notification(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = NotifyForm(request.POST)
        if form.is_valid():
            messages.success(request, "Нотификация успешно отправлена")
            form.save()
        else:
            print form.errors
    else:
        form = NotifyForm()
    return render(request, "org/notify.html", {
        "form": form,
        "notifies": Notification.objects.filter(houses__in=request.user.company.houses.all()).prefetch_related().distinct(),
        "houses": request.user.company.houses.all()
    })


def delete_notification(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddNotificationForm(request.POST)
        if form.is_valid():
            Notification.objects.filter(houses__company=request.user.company, id=form.cleaned_data['notify']).delete()
        else:
            print form.errors
    return redirect(reverse("create_notification"))


def list_houses(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    return render(request, "org/houses.html", {
        "houses": request.user.company.houses.all(),
        "form": AddHouseForm(),
    })


def delete_house(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddHouseForm(request.POST)
        if form.is_valid():
            request.user.company.houses.remove(House.objects.get(id=form.cleaned_data['house']))
    return redirect(reverse("list_houses"))


def add_house(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddHouseForm(request.POST)
        if form.is_valid():
            request.user.company.houses.add(House.objects.get(id=form.cleaned_data['house']))
    return redirect(reverse("list_houses"))


def list_residents(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    return render(request, "org/residents.html", {
        "residents": Resident.objects.filter(house__id__in=request.user.company.houses.all()),
        "form": AddResidentForm(),
    })


def delete_resident(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddNotificationForm(request.POST)
        if form.is_valid():
            Resident.objects.filter(id=form.cleaned_data['notify'], houses__company=request.user.company).delete()
    return redirect(reverse("list_residents"))


def userprofile(request):
    if is_org(request.user):
        return redirect(reverse("orghome"))
    profile = ResidentForm(data=model_to_dict(Resident.objects.get(user=request.user)))
    return render(request, "user/profile.html", {
        "profile": profile,
    })


def register(request):
    return common_registration(request, ResidentForm, 'user/registration.html')


def logoutview(request):
    logout(request)
    return redirect(reverse('home'))
