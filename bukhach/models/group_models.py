from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from bukhach.utils.common_utils import make_filepath


class Gathering(models.Model):
    users = ManyToManyField(User, verbose_name="Users")
    group_avatar = models.ImageField(upload_to=make_filepath, verbose_name="group_avatar", default="def_group_ava.jpeg")
    group_creator = ForeignKey(User, verbose_name="Group creator", on_delete=models.CASCADE, related_name="YourGroups")


class GroupApplication(models.Model):
    group = ForeignKey(Gathering, verbose_name="Group", on_delete=models.CASCADE)
    applicant = ForeignKey(User, verbose_name="Applacant", on_delete=models.CASCADE)