from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from bukhach.models.gathering_models import Gathering


class UserInterval(models.Model):
    user = ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Start date')
    end_date = models.DateTimeField(verbose_name='End date')
    gathering = ForeignKey(Gathering, verbose_name="Gathering", on_delete=models.CASCADE, blank=True, default=None)


class GatheringInterval(models.Model):
    start_matched_date = models.DateTimeField(verbose_name="Start matched date")
    end_matched_date = models.DateTimeField(verbose_name="End matched date")
    gathering = ForeignKey(Gathering,  verbose_name="Gathering", on_delete=models.CASCADE)