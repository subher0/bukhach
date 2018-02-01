from django.http import HttpResponse
from django.template import loader

from bukhach.forms import IntervalForm, PeopleSearchForm
from bukhach.models.matcher_models import UserInterval
from bukhach.models.profile_models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def dashboard_view(request, humans = None):
    template = loader.get_template('bukhach/dashboard/dashboard.html')
    user = request.user
    intervals = UserInterval.objects.filter(user=user)
    profile = Profile.objects.filter(user=user).first()
    friends = profile.friends.all()
    context = {
        'intervals': intervals,
        'profile': profile,
        'friends': friends,
        'humans': humans
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


def people_search(request):
    form = PeopleSearchForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data['nameField']
        name_list = name.split()
        f_name = name_list[0]
        l_name = name_list[1]
        humans = User.objects.filter(first_name=f_name, last_name=l_name)
        return dashboard_view(request, humans)


def profile_view(request, profileId):
    template = loader.get_template('bukhach/profile.html')
    profile = Profile.objects.filter(id=profileId).first()
    friends = profile.friends.all()
    context = {
        'profile': profile,
        'friends': friends
    }
    return HttpResponse(template.render(context, request))
