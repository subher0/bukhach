from django import forms


class RegisterForm(forms.Form):
    first_nameField = forms.CharField(label='first name', max_length=20)
    last_nameField = forms.CharField(label='last name', max_length=20)
    usernameField = forms.CharField(label='username', max_length=20)
    emailField = forms.CharField(label='email', max_length=20)
    passwordField = forms.CharField(label='password', max_length=20)


class LoginForm(forms.Form):
    usernameField = forms.CharField(label='username', max_length=20)
    passwordField = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)


class IntervalForm(forms.Form):
    start_interval = forms.DateTimeField(label='start', input_formats=['%Y-%m-%dT%H:%M'])
    end_interval = forms.DateTimeField(label='end', input_formats=['%Y-%m-%dT%H:%M'])


class PeopleSearchForm(forms.Form):
    nameField = forms.CharField(label='name', max_length=41)


class AddFriendForm(forms.Form):
    profile_id = forms.IntegerField(label='profile id')


class DeleteFriendForm(forms.Form):
    profile_id = forms.IntegerField(label='profile id')