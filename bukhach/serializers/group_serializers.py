from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.group_models import Gathering


# class GatheringSerializer(serializers.ModelSerializer):
#     users = UserMinSerializer()
#
#     def create(self, validated_data):
#         custom_group = Gathering(**validated_data)
#         custom_group.save()
#         return custom_group
#
#
#     class Meta:
#         model = Gathering
#         fields = ('users', 'group_avatar')
#
#
# class GatheringIntervalSerializer(serializers.ModelSerializer):
#     group = GatheringSerializer()
#
#     class Meta:
#         model = GatheringInterval
#         fields = ('group', 'start_matched_date', 'end_matched_date')
