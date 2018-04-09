from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from bukhach.forms import IntervalForm, PeopleSearchForm, ProfileEditForm, AvatarEditForm, PasswordEditForm
from bukhach.models.interval_models import UserInterval
from bukhach.models.profile_models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q


@login_required(login_url='/login')
def dashboard_view(request, error_message=None, humans=None):
    template = loader.get_template('bukhach/dashboard/dashboard.html')
    user = request.user
    intervals = UserInterval.objects.filter(user=user)
    profile = Profile.objects.filter(user=user).first()
    friends = profile.friends.all()
    form = ProfileEditForm(data={'username_field': user.username,
                                 'email_field': user.email,
                                 'tel_num_field': profile.tel_num,
                                 'info_field': profile.info})
    password_edit_form = PasswordEditForm()
    context = {
        'intervals': intervals,
        'profile': profile,
        'friends': friends,
        'humans': humans,
        'form': form,
        'password_edit_form': password_edit_form,
        'error_message': error_message
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


#Временнная хуйня поправить!!11!1!1!1!!
def people_search(request):
    form = PeopleSearchForm(request.GET)
    if form.is_valid():
        search_request = form.cleaned_data['nameField']
        words = search_request.split()
        if len(words) == 1:
            name = words[0]
            humans = User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
            return dashboard_view(request, humans=humans)
        elif len(words) == 2:
            f_name = words[0]
            l_name = words[1]
            humans = User.objects.filter(first_name__icontains =f_name, last_name__icontains=l_name)
            return dashboard_view(request, humans=humans)
        else:
            return redirect('/gtfo')


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            user = request.user
            profile = request.user.profile
            profile.tel_num = form.cleaned_data['tel_num_field']
            profile.info = form.cleaned_data['info_field']
            user.username = form.cleaned_data['username_field']
            user.email = form.cleaned_data['email_field']
            user.save()
            profile.save()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')


def edit_avatar(request):
    if request.method == 'POST':
        form = AvatarEditForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.avatar = form.cleaned_data['avatar_field']
            profile.save()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')


def edit_password(request):
    if request.method == 'POST':
        form = PasswordEditForm(request.POST)
        if form.is_valid():
            user = request.user
            old_pass = form.cleaned_data['old_pass_field']
            f_pass = form.cleaned_data['first_pass_field']
            s_pass = form.cleaned_data['second_pass_field']
            if check_password(old_pass, user.password):
                if f_pass == s_pass:
                    user.set_password(f_pass)
                    user.save()
                    return redirect('/dashboard')
                else:
                    return dashboard_view(request, error_message='Пароли не совпадают')
            else:
                return dashboard_view(request, error_message='Неверный пароль')
        else:
            dashboard_view(request, error_message='Твоя форма инвалид')
    else:
        dashboard_view(request, error_message='ГЕТ не пройдет')
