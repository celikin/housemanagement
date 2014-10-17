from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

def home(request):
    return render(request, "home.html")

def registration(request):
	if request.user.is_authenticated():
		return redirect(reverse('home'))
	else:
		return render(request, "registration.html")

def register(request):
	return redirect(reverse('home'))