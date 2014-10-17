# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CompanyForm, ResidentForm

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
    return render(request, "orgregistration.html", {
        "form": form
    })


def orgregistration(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == "POST":
        pass
    form = CompanyForm()
    return render(request, "orgregistration.html", {
        "form": form
    })


def register(request):
	return redirect(reverse('home'))
