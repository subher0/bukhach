from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField, ForeignKey, OneToOneField

from bukhach.models.profile_models import Profile
from bukhach.utils.common_utils import make_filepath


class Gathering(models.Model):
    name = models.CharField(max_length=64, verbose_name='Gathering name', default='Gay gathering')
    users = ManyToManyField(Profile, verbose_name="Users", related_name='gatherings')
    gathering_avatar = models.ImageField(upload_to=make_filepath, verbose_name="Gathering avatar", default="def_group_ava.jpeg")
    gathering_creator = ForeignKey(Profile, verbose_name="Gathering creator", on_delete=models.CASCADE, related_name="YourGatherings")

    def __str__(self):
        return '_'.join([str(self.id), self.name])


class GatheringApplication(models.Model):
    gathering = ForeignKey(Gathering, verbose_name="Gathering", on_delete=models.CASCADE, related_name='applications')
    applicant = ForeignKey(Profile, verbose_name="Applicant", on_delete=models.CASCADE)

    def __str__(self):
        return '_'.join([self.gathering.name, str(self.gathering.id), self.applicant.user.username])