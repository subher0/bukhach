from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField, OneToOneField
from bukhach.utils.common_utils import make_filepath


class Profile(models.Model):
    def __str__(self):
        return self.user.username

    user = OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    info = models.TextField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to=make_filepath, verbose_name='avatar', default='def_ava.png')
    rating = models.FloatField(verbose_name='rating', max_length=2, default=0.0)
    friends = ManyToManyField('self', verbose_name='friends', blank=True)
    tel_num = models.CharField(max_length=21, blank=True, verbose_name='tel_num')

