from django.http import HttpResponse
from django.template import loader
from bukhach.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from bukhach.models.profile_models import Profile

from bukhach.views import page_views, dashboard_views


def register_view(request):
    if request.method == 'POST':
       return register_user(request)
    template = loader.get_template('bukhach/register.html')
    context = {}
    return HttpResponse(template.render(context, request))


def register_user(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = User.objects.create_user(form.cleaned_data['usernameField'],
                                        form.cleaned_data['emailField'], form.cleaned_data['passwordField'])
        user.first_name = form.cleaned_data['first_nameField']
        user.last_name = form.cleaned_data['last_nameField']
        user.save()
        profile = Profile(user=user).save()
        return redirect('/login')


def login_view(request, error_message=None):
    template = loader.get_template('bukhach/login.html')
    context = {
        'error_message': error_message
    }
    return HttpResponse(template.render(context, request))


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['usernameField'], password = form.cleaned_data['passwordField'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/dashboard')
                else:
                    return login_view(request, error_message='Юзер неактивен, гг')
            else:
                return login_view(request, error_message='Пользователь с таким именем или паролем не найден')
        else:
            return login_view(request, error_message='Неправильно заполнена форма')
    else:
        return login_view(request, error_message='Поддерживается только POST запрос!')



def logout_user(request):
    if request.method == 'POST':
        logout(request)
    return page_views.index_view(request)
