from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from bukhach.models.group_models import Gathering


class UserInterval(models.Model):
    user = ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Start date')
    end_date = models.DateTimeField(verbose_name='End date')
    group_id = ForeignKey(Gathering, verbose_name="Group", on_delete=models.CASCADE, blank=True, default=None)


class GroupInterval(models.Model):
    start_matched_date = models.DateTimeField(verbose_name="Start matched date")
    end_matched_date = models.DateTimeField(verbose_name="End matched date")
    group = ForeignKey(Gathering,  verbose_name="Group", on_delete=models.CASCADE)