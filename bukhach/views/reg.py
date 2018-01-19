from bukhach.bukhach.reg_form import Register_form
from django.contrib.auth.models import User


def reg(request):
    form = Register_form()

    if request.method == 'POST':
        form = Register_form(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.first_nameField, form.emailField, form.passwordField)

    
