from django.http import HttpResponse
from django.template import loader


def index_view(request):
    template = loader.get_template('site/index.html')
    context = {
        "ip": request.META['HTTP_X_REAL_IP']
    }
    return HttpResponse(template.render(context, request))


def about_us_view(request):
    template = loader.get_template('site/about_us.html')
    context = {
        "ip": request.META['HTTP_X_REAL_IP']
    }
    return HttpResponse(template.render(context, request))


def match_view(request):
    template = loader.get_template('site/match.html')
    context = {
        "ip": request.META['HTTP_X_REAL_IP']
    }
    return HttpResponse(template.render(context, request))
