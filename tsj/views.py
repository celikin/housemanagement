# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CompanyForm
from django.contrib.auth.models import User


def home(request):
    if not request.user.is_authenticated():
        return render(request, "home.html")
    return render(request, "userhome.html")


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
    return render(request, "registration.html", {
        "form": form
    })


def orgregistration(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.save()
            form.cleaned_data['user'] = user
            messages.success(request, 'Вы успешно зарегестрированы. Ожидайте подтверждения')
            form.save()
            return redirect(reverse('home'))
    else:
        form = CompanyForm()
    return render(request, "orgregistration.html", {
        "form": form
    })


def register(request):
	return redirect(reverse('home'))
