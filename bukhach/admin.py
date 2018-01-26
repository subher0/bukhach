from django.contrib import admin

# Register your models here.
from bukhach.models.matcher_models import UserInterval
from bukhach.models.profile_models import Profile

admin.site.register(UserInterval)
admin.site.register(Profile)
