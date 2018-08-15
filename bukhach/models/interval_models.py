import datetime

from django.db import models
from django.db.models import ForeignKey, OneToOneField
from bukhach.models.gathering_models import Gathering
from bukhach.models.profile_models import Profile
from bukhach.utils.common_utils import transform_time


class UserInterval(models.Model):
    user = ForeignKey(Profile, verbose_name="User", on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Start date')
    end_date = models.DateTimeField(verbose_name='End date')
    gathering = ForeignKey(Gathering, db_column='gathering_id', verbose_name="Gathering", on_delete=models.CASCADE, null=True, default=None)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.start_date = transform_time(self.start_date)
        self.end_date = transform_time(self.end_date)
        if self.gathering_id:
            GatheringInterval.objects.filter(gathering_id=self.gathering_id).delete()
        super(UserInterval, self).save()

    def __str__(self):
        return self.user.user.username + '___' + str(self.id)


class GatheringInterval(models.Model):
    start_date = models.DateTimeField(verbose_name="Start date")
    end_date = models.DateTimeField(verbose_name="End date")
    gathering = ForeignKey(Gathering,  verbose_name="Gathering", on_delete=models.CASCADE, related_name='intervals')

    def __str__(self):
        return '___'.join([self.gathering.name, str(self.id)])
