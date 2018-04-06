from django.contrib import admin

# Register your models here.
from bukhach.models.interval_models import UserInterval, GroupInterval
from bukhach.models.profile_models import Profile
from bukhach.models.group_models import CustomGroup, GroupApplication

admin.site.register(UserInterval)
admin.site.register(Profile)
admin.site.register(GroupInterval)
admin.site.register(CustomGroup)
admin.site.register(GroupApplication)
