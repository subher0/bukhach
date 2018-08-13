from rest_framework import serializers

from bukhach.models.profile_models import Profile
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.gathering_models import Gathering, GatheringApplication
from bukhach.serializers.user_serializers import ProfileMinSerializer


class GatheringMaxSerializer(serializers.ModelSerializer):
    users = ProfileMinSerializer(many=True, read_only=True)
    gathering_creator = ProfileMinSerializer(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)

    def create(self, validated_data):
        name = validated_data.get('name', None)
        avatar = validated_data.get('avatar', None)
        gathering = Gathering.objects.create(gathering_creator=validated_data['creator'])
        if avatar:
            gathering.gathering_avatar = avatar
        if name:
            gathering.name = name
        gathering.users.add(validated_data['creator'])
        gathering.save()
        return gathering

    class Meta:
        model = Gathering
        fields = ('id', 'users', 'gathering_avatar', 'name', 'gathering_creator', 'creator')


class GatheringApplicationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        app = GatheringApplication.objects.create(**validated_data)
        return app

    class Meta:
        model = GatheringApplication
        fields = ('id', 'applicant', 'gathering')
        read_only_fields = ('id',)


class GatheringMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gathering
        fields = ('id', 'gathering_avatar', 'name')
