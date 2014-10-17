from django.forms import ModelForm
from .models import Company


class ArticleForm(ModelForm):

    class Meta:
        model = Company
