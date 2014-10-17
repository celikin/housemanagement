# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CompanyForm, ResidentForm
from .models import Resident, Company
from django.contrib.auth.models import User
from django.contrib.auth import logout


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
    return render(request, "userhome.html")


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


def orgregistration(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            user.save()
            company = form.save(commit=False)
            company.user = user
            messages.success(request, 'Вы успешно зарегестрированы. Ожидайте подтверждения')
            company.save()
            return redirect(reverse('home'))
    else:
        form = CompanyForm()
    return render(request, "org/registration.html", {
        "form": form
    })


def register(request):
	return redirect(reverse('home'))


def logoutview(request):
    logout(request)
    return redirect(reverse('home'))