from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.group_models import Gathering
from bukhach.serializers.user_serializers import UserSerializer


class GatheringSerializer(serializers.ModelSerializer):
    #users = UserSerializer()

    def create(self, validated_data):
        name = validated_data.get('name', None)
        avatar = validated_data.get('avatar', None)
        gathering = Gathering.objects.create(gathering_creator=validated_data['gathering_creator'])
        if avatar:
            gathering.gathering_avatar = avatar
        if name:
            gathering.name = name
        for user in validated_data['users']:
            gathering.users.add(user)
        gathering.save()
        return gathering.id


    class Meta:
        model = Gathering
        fields = ('users', 'gathering_avatar', 'name', 'gathering_creator')


class GatheringIntervalSerializer(serializers.ModelSerializer):
    group = GatheringSerializer()

    class Meta:
        model = GatheringInterval
        fields = ('group', 'start_matched_date', 'end_matched_date')
