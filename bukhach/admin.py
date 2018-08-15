from django.contrib import admin

# Register your models here.
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.profile_models import Profile, Invite
from bukhach.models.gathering_models import Gathering, GatheringApplication


class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rating', 'tel_num')
    search_fields = ('username', 'email', 'tel_num')
    ordering = ('rating',)
    list_select_related = ('user',)

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


class CustomUserIntervalAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'gathering')
    list_filter = ('user', 'gathering')


class CustomGatheringIntervalAdmin(admin.ModelAdmin):
    list_display = ('gathering', 'start_date', 'end_date')
    list_filter = ('gathering',)


class CustomGatheringAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'gathering_creator', 'users_count')
    list_filter = ('gathering_creator',)
    search_fields = ('name',)

    def users_count(self, obj):
        return obj.users.all().count()


class CustomGatheringApplicationAdmin(admin.ModelAdmin):
    list_display = ('gathering', 'applicant')
    list_filter = ('gathering',)


admin.site.register(UserInterval, CustomUserIntervalAdmin)
admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(GatheringInterval, CustomGatheringIntervalAdmin)
admin.site.register(Gathering, CustomGatheringAdmin)
admin.site.register(GatheringApplication, CustomGatheringApplicationAdmin)
admin.site.register(Invite)
