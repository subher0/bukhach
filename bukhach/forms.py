from django import forms

class RegisterForm(forms.Form):
    first_nameField = forms.CharField(label='first_name', max_length=20)
    last_nameField = forms.CharField(label='last_name', max_length=20)
    emailField = forms.CharField(label='email', max_length=20)
    passwordField = forms.CharField(label='password', max_length=20)

