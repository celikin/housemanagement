from django.core.urlresolvers import resolve


def current_url(request):
    return {"current_url": resolve(request.path_info).url_name}
