from django.http import HttpResponse
from django.template import loader

from bukhach.forms import RegisterForm
from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        register_user(request)
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

def login_view(request):
    if request.method == 'POST':
        login_user(request)
    template = loader.get_template('bukhach/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

