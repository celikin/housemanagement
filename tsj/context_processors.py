from django.core.urlresolvers import resolve
from .models import Resident


def current_url(request):
    return {"regcounter": Resident.objects.filter(user__is_active=False).count()}


def interface(request):
    return {"current_url": resolve(request.path_info).url_name}
