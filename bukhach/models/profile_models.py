import base64
import re
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField, OneToOneField

from bukhach.utils.common_utils import make_filepath


class Profile(models.Model):
    user = OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    info = models.TextField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to=make_filepath, verbose_name='avatar', default='def_ava.png')
    rating = models.FloatField(verbose_name='rating', max_length=2, default=0.0)
    friends = ManyToManyField('self', verbose_name='friends', blank=True)
    tel_num = models.CharField(max_length=21, blank=True, verbose_name='tel_num')
    last_ip = models.CharField(max_length=16, verbose_name='Last IP adress', blank=True, default=None, null=True)

    def __str__(self):
        return self.user.username


def generate_invitation_code():
    return (base64.b64encode(re.sub('-', '', str(uuid.uuid4()) + str(uuid.uuid4())).encode('ascii'))).decode('utf-8')


class Invite(models.Model):
    user = OneToOneField(User, verbose_name='User', editable=False, on_delete=models.CASCADE, blank=True, null=True)
    invitation_code = models.CharField(db_index=True, max_length=255, blank=False, null=False,
                                      default=generate_invitation_code)

    def __str__(self):
        return (self.user.username if self.user is not None else 'Free invite code') + ' ' + self.invitation_code

