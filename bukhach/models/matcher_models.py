from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


class UserInterval(models.Model):
    user = ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Start date')
    end_date = models.DateTimeField(verbose_name='End date')