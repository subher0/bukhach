from django.http import HttpResponse
from django.template import loader


def dashboard_view(request):
    template = loader.get_template('bukhach/dashboard/dashboard.html')
    context = {}
    return HttpResponse(template.render(context, request))