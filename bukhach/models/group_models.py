from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from bukhach.utils.common_utils import make_filepath


class Gathering(models.Model):
    users = ManyToManyField(User, verbose_name="Users")
    gathering_avatar = models.ImageField(upload_to=make_filepath, verbose_name="Gathering avatar", default="def_group_ava.jpeg")
    gathering_creator = ForeignKey(User, verbose_name="Gathering creator", on_delete=models.CASCADE, related_name="YourGatherings")


class GatheringApplication(models.Model):
    gathering = ForeignKey(Gathering, verbose_name="Gathering", on_delete=models.CASCADE)
    applicant = ForeignKey(User, verbose_name="Applacant", on_delete=models.CASCADE)