from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, ManyToManyField, OneToOneField


class Profile(models.Model):
    def __str__(self):
        return self.user.username

    user = OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    info = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='static/img/avatars', verbose_name='avatar', default='def_ava.png')
    rating = models.FloatField(verbose_name='rating', max_length=2, default=0.0)
    friends = ManyToManyField('self', verbose_name='friends', blank=True)
