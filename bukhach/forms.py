from django import forms


class RegisterForm(forms.Form):
    first_name_field = forms.CharField(label='Имя', max_length=20)
    last_name_field = forms.CharField(label='Фамилия', max_length=20)
    username_field = forms.CharField(label='Имя пользователя', max_length=20)
    email_field = forms.CharField(label='Email', max_length=20)
    password_field = forms.CharField(label='Пароль', max_length=20, widget=forms.PasswordInput)
    tel_num_field = forms.CharField(label='Номер телефона', max_length=21)
    avatar_field = forms.ImageField(required=False)


class LoginForm(forms.Form):
    username_field = forms.CharField(label='username', max_length=20)
    password_field = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)


class IntervalForm(forms.Form):
    start_interval = forms.DateTimeField(label='start', input_formats=['%Y-%m-%dT%H:%M'])
    end_interval = forms.DateTimeField(label='end', input_formats=['%Y-%m-%dT%H:%M'])


class PeopleSearchForm(forms.Form):
    nameField = forms.CharField(label='name', max_length=41)


class AddFriendForm(forms.Form):
    profile_id = forms.IntegerField(label='profile id')


class DeleteFriendForm(forms.Form):
    profile_id = forms.IntegerField(label='profile id')


class ProfileEditForm(forms.Form):
    username_field = forms.CharField(label='Имя пользователя', max_length=20)
    email_field = forms.CharField(label='Email', max_length=20)
    tel_num_field = forms.CharField(label='Номер телефона', max_length=21, required=False)
    info_field = forms.CharField(label='О себе', required=False, widget=forms.Textarea)


class AvatarEditForm(forms.Form):
    avatar_field = forms.ImageField(required=False)


class PasswordEditForm(forms.Form):
    old_pass_field = forms.CharField(label='Текущий пароль', max_length=20, widget=forms.PasswordInput)
    first_pass_field = forms.CharField(label='Новый пароль', max_length=20, widget=forms.PasswordInput)
    second_pass_field = forms.CharField(label='Повторите новый пароль', max_length=20, widget=forms.PasswordInput)