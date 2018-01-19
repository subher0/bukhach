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
        user = User.objects.create_user(form.cleaned_data['first_nameField'],
                                        form.cleaned_data['emailField'], form.cleaned_data['passwordField'])
        user.save()
