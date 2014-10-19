# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
import datetime as dt
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import json
import time
from django.utils import timezone

from .forms import *
from .models import Resident, Company, House, Notification, MeterReadingHistory, MeterType
from .models import ServiceCompany, Employer
from .streets import STREET_CHOICES

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
    calendar = []
    timezone.make_aware(dt.datetime.now(), timezone.get_default_timezone())
    for i in range(27):
        date = timezone.now() + dt.timedelta(days=i)
        calendar.append({"date": date, "events": [], "dayofweek": _date(date, "D")[:-1].upper()})

    notes = request.user.resident.house.notification_set.filter(end_date__lte=timezone.now()+dt.timedelta(days=27),
            start_date__gt=timezone.now()-dt.timedelta(days=1))

    for note in notes:
        delta1 = note.end_date - note.start_date
        delta2 = note.end_date - timezone.now()
        for i in range(delta1.days):
            calendar[delta2.days - i]["events"].append(note)
    return render(request, "user/home.html", {
        "resident": request.user.resident,
        "calendar": calendar,
        "org": request.user.resident.house.company_set.all()[0],
    })


def orghome(request):
    if not request.user.is_authenticated() or not is_org(request.user):
        return redirect(reverse("home"))
    if not is_org(request.user):
        return redirect(reverse("home"))
    return redirect(reverse("list_houses"))
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
        	messages.error(request, "Ваш аккаунт еще не подтвержден")
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
            user = User(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
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


def add_services(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddServiceCompanyForm(request.POST)
        if form.is_valid():
            request.user.company.services.add(ServiceCompany.objects.get(id=form.cleaned_data['service']))
    else:
        form = AddServiceCompanyForm()
    return render(request, "org/add_services.html", {
        "services":  request.user.company.services.all(),
        "employers":  request.user.company.employer_set.all(),
        "form": form,
        "emplform": EmployerForm(),
    })


def add_employer(request):
    if request.method == "POST":
        form = EmployerForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.company = request.user.company
            emp.save()
    return redirect("add_services")


def delete_employer(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddServiceEmployerForm(request.POST)
        if form.is_valid():
            request.user.company.employers.remove(Employer.objects.get(id=form.cleaned_data['employer']))
    return redirect(reverse("add_services"))


def delete_services(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddServiceCompanyForm(request.POST)
        if form.is_valid():
            print 'yay'
            request.user.company.services.remove(ServiceCompany.objects.get(id=form.cleaned_data['service']))
        else:
            print form.errors
    return redirect(reverse("add_services"))


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
        "jchoices": json.dumps(STREET_CHOICES),
    })


def delete_house(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddHouseForm(request.POST)
        request.user.company.houses.remove(House.objects.get(
            pk=form.data["house"]))
    return redirect(reverse("list_houses"))


def add_house(request):
    if not is_org(request.user):
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AddHouseForm(request.POST)
        if form.is_valid():
            # ATTENTOIN not tred-saif!!111
            h = House.objects.get_or_create(
                street=form.cleaned_data['street'],
                number=form.cleaned_data['number'])
            request.user.company.houses.add(h[0])
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

def userapprove(request):
	c = Company.objects.get(user=request.user)
	users = c.get_residents().filter(user__is_active=False)
	return render(request, "org/user_approve.html", {
		"users": users,
	})

def sendmail(request, pk, state):

	user = Resident.objects.get(pk=pk)
	name = user.last_name + " " + user.first_name
	email = user.user.email

	if state:
		path = "welcome_email.html"
		user.user.is_active = True
		user.user.save()
	else:
		path = "reject_email.html"
		user.delete()

	send_mail(
		'Cпасибо за регистрацию',
		get_template(path).render(
			Context({
				'username': name,
			})
		),
		'larkina.bad@gmail.com',
		[email],
		fail_silently = False
	)
	return userapprove(request)

def sendreject(request, pk):
	return sendmail(request, pk, False)

def sendwelcome(request, pk):
	return sendmail(request, pk, True)

def meter(request):

    if request.method == "POST":
        form = MeterForm(request.POST)
        if form.is_valid():

            resident = Resident.objects.get(user=request.user)
            meter_type = MeterType.objects.get(pk=form.cleaned_data['meter_type'])

            hist = MeterReadingHistory.objects.filter(resident=resident)
            for h in hist:
                if h.meter_type==meter_type and datetime.now().strftime("%B")==h.adding_date.strftime("%B"):
                	messages.error(request, u"Вы уже внесли показания %s за этот месяц, удалите старые" % meter_type.name)
                	return redirect(reverse('meter'))

            entity = form.save(commit=False)
            entity.meter_type=meter_type
            entity.resident = resident
            messages.success(request, 'Показания приняты')
            entity.save()
            return redirect(reverse('meter'))
    else:
        form = MeterForm()

    res = Resident.objects.filter(user=request.user)
    hist = MeterReadingHistory.objects.filter(resident=res)

    have_type = []
    for h in hist:
        if datetime.now().strftime("%B")==h.adding_date.strftime("%B"):
            have_type += [h.meter_type.name]

    need = MeterType.objects.exclude(name__in=have_type)

    chart_data = dict()
    for t in MeterType.objects.all():
    	chart_data[t.id] = hist.filter(meter_type=t)

    return render(request, "user/meter_reading.html", {
        "form": form,
        "hist": hist,
        "need": need,
        "chart_data": chart_data,
        "meter_names": MeterType.objects.all()
    })

def house_account(request, pk):

    if request.method == "POST":
        form = HouseAccountForm(request.POST)
        if form.is_valid():

            house = House.objects.get(pk=pk)
            entity = form.save(commit=False)
            entity.house = house
            messages.success(request, 'Запись добавлена')
            entity.save()
            return redirect(reverse('houseaccount', kwargs={'pk':pk}))
    
    form = HouseAccountForm()
    house = House.objects.filter(pk=pk)
    hist = HouseAccount.objects.filter(house=house)

    account = 0
    for h in hist:
        account += h.account_change

    return render(request, "org/house_account.html", {
        "form": form,
        "hist": hist,
        "pk": pk,
        "sum": account,
	})

def auth_api(request):

    if request.method != 'POST':
        return HttpResponse('Unauthorized', status=401)

    username = request.DATA['username']
    password = request.DATA['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Unauthorized', status=401)

    try:
        res = Resident.objects.get(user=user)
        c = Company.objects.filter(houses=res.house)
    except Exception, e:
        return HttpResponse('Unauthorized', status=401)
    
    data =  {"id": user.id, "id_company":c.id}
    return HttpResponse(json.dumps(data), content_type="application/json")

def news_api(request, company_id):
    company = Company.objects.filter(pk=company_id)
    if not company:
        HttpResponse('Unauthorized', status=401)

    company = company[0]
    news = Notification.objects.filter(houses__in=company.houses.all())
    
    res = []
    for n in news:
        res += [ {
            "main": n.text,
            "header": n.note_type,
            "date": int(time.mktime(n.pub_date.timetuple())*1000)
        }]
    return HttpResponse(json.dumps(res), content_type="application/json")


def employer_request(request):

    if request.method == "POST":
        form = EmployerRequestForm(request.POST)
        if form.is_valid():

            employer = Employer.objects.get(pk=form.cleaned_data['employer'])
            res = Resident.objects.get(user=request.user)
            entity = form.save(commit=False)
            entity.employer = employer
            entity.user = res
            entity.request_date = form.data.get('request_date', datetime.now())
            messages.success(request, u"Ваша заявка принята! Ожидайте звонка")
            entity.save()
            return redirect(reverse('employer_request'))

    form = EmployerRequestForm()
    res = Resident.objects.filter(user=request.user)
    hist = EmployerRequest.objects.filter(user=res)
    return render(request, "user/employer_request.html", {
        "form": form,
        "hist": hist,
    })


def org_employer_request(request):

    hist = EmployerRequest.objects.all()
    return render(request, "org/employer_request.html", {
        "hist": hist,
    })    


def delete_emp_req(request, pk):
    emp = EmployerRequest.objects.filter(pk=pk)

    if emp:
        emp.delete()

    return redirect(reverse('employer_request'))

def approve_emp_req(request, pk):
    emp = EmployerRequest.objects.get(pk=pk)

    emp.status = True
    emp.save()
    return redirect(reverse('org_employer_request'))
