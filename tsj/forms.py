from django.forms import ModelForm
from .models import Company, Resident


class CompanyForm(ModelForm):

    class Meta:
        model = Company


class ResidentForm(ModelForm):

    class Meta:
        model = Resident