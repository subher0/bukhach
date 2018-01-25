from django.http import HttpResponse
from django.template import loader

from bukhach.forms import IntervalForm
from bukhach.models.matcher_models import UserInterval
from bukhach.models.profile_models import Profile


def dashboard_view(request):
    template = loader.get_template('bukhach/dashboard/dashboard.html')
    user = request.user
    intervals = UserInterval.objects.filter(user=user)
    context = {
        'intervals': intervals,
    }
    return HttpResponse(template.render(context, request))


def accept_interval(request):
    if request.method == 'POST':
        form = IntervalForm(request.POST)
        if form.is_valid():
            userInterval = UserInterval(user=request.user, start_date=form.cleaned_data['start_interval'],
                                        end_date=form.cleaned_data['end_interval'])
            userInterval.save()
    return dashboard_view(request)

