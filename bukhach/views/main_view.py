from django.http import HttpResponse
from django.template import loader


def index_view(request):
    template = loader.get_template('bukhach/index.html')
    context = {
        "ip": request.META['HTTP_X_REAL_IP']
    }
    return HttpResponse(template.render(context, request))


def about_us_view(request):
    template = loader.get_template('bukhach/about_us.html')
    context = {}
    return HttpResponse(template.render(context, request))


def match_view(request):
    template = loader.get_template('bukhach/match.html')
    context = {}
    return HttpResponse(template.render(context, request))


def contacts_view(request):
    template = loader.get_template('bukhach/contacts.html')
    context = {}
    return HttpResponse(template.render(context, request))


def register_view(request):
    template = loader.get_template('bukhach/register.html')
    context = {}
    return HttpResponse(template.render(context, request))