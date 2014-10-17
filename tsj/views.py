# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CompanyForm, ResidentForm
from .models import Resident, Company
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.forms.models import model_to_dict


def is_org(user):
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
            company.save()
            return redirect(reverse('home'))
    else:
        form = Form()
    return render(request, template, {
        "form": form
    })


def orgregistration(request):
    return common_registration(request, CompanyForm, 'org/registration.html')


def orgprofile(request):
    profile = CompanyForm(data=model_to_dict(Company.objects.get(user=request.user)))
    return render(request, "org/profile.html", {
        "profile": profile,
    })


def userprofile(request):
    profile = ResidentForm(data=model_to_dict(Resident.objects.get(user=request.user)))
    return render(request, "user/profile.html", {
        "profile": profile,
    })


def register(request):
    return common_registration(request, ResidentForm, 'user/registration.html')

def logoutview(request):
    logout(request)
    return redirect(reverse('home'))
