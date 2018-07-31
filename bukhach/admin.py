from django.contrib import admin

# Register your models here.
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.profile_models import Profile
from bukhach.models.gathering_models import Gathering, GatheringApplication

admin.site.register(UserInterval)
admin.site.register(Profile)
admin.site.register(GatheringInterval)
admin.site.register(Gathering)
admin.site.register(GatheringApplication)
