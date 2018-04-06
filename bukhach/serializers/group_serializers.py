from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile
from bukhach.models.interval_models import UserInterval, GroupInterval
from bukhach.models.group_models import CustomGroup


# class CustomGroupSerializer(serializers.ModelSerializer):
#     users = UserSerializer()
#
#     def create(self, validated_data):
#         custom_group = CustomGroup(**validated_data)
#         custom_group.save()
#         return custom_group
#
#
#     class Meta:
#         model = CustomGroup
#         fields = ('users', 'group_avatar')
#
#
# class GroupIntervalSerializer(serializers.ModelSerializer):
#     group = CustomGroupSerializer()
#
#     class Meta:
#         model = GroupInterval
#         fields = ('group', 'start_matched_date', 'end_matched_date')
