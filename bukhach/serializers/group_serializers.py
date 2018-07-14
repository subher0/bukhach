from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.gathering_models import Gathering, GatheringApplication
from bukhach.serializers.user_serializers import UserSerializer, MinUserSerializer, MinProfileSerializer


class GatheringCreateSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = GatheringInterval
        fields = ('start_matched_date', 'end_matched_date')


class GatheringApplicationSerializer(serializers.ModelSerializer):
    applicant = MinProfileSerializer()

    class Meta:
        model = GatheringApplication
        fields = ('id', 'applicant')


class GatheringFullGetSerializer(serializers.ModelSerializer):
    users = MinProfileSerializer(many=True)
    interval = GatheringIntervalSerializer()
    applications = GatheringApplicationSerializer(many=True)

    class Meta:
        model = Gathering
        fields = ('id', 'users', 'gathering_avatar', 'name', 'interval', 'applications')


class GatheringMinGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gathering
        fields = ('id', 'gathering_avatar', 'name')


class GatheringUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gathering
        fields = ('id', 'gathering_avatar', 'name')
