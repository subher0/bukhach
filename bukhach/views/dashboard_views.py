from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from bukhach.forms import IntervalForm, PeopleSearchForm, ProfileEditForm
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
    form = ProfileEditForm(data={'username_field': user.username,
                                 'email_field': user.email,
                                 'tel_num_field': profile.tel_num})
    context = {
        'intervals': intervals,
        'profile': profile,
        'friends': friends,
        'humans': humans,
        'form': form
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


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            user = request.user
            profile = request.user.profile
            profile.tel_num = form.cleaned_data['tel_num_field']
            user.username = form.cleaned_data['username_field']
            user.email = form.cleaned_data['email_field']
            user.save()
            profile.save()
            return dashboard_view(request)
        else:
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')