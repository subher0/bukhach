from rest_framework import serializers
from rest_framework.fields import BooleanField, SerializerMethodField, empty

from bukhach.models.profile_models import Profile
from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.models.gathering_models import Gathering, GatheringApplication
from bukhach.serializers.user_serializers import ProfileMinSerializer, ProfileMedSerializer


class GatheringMaxSerializer(serializers.ModelSerializer):
    users = ProfileMinSerializer(many=True, read_only=True)
    gathering_creator = ProfileMinSerializer(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    is_owned = SerializerMethodField()
    is_available_for_join = SerializerMethodField()
    has_applied_for_join = SerializerMethodField()
    is_member = SerializerMethodField()

    def __init__(self, instance=None, data=empty, user=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self._has_applied_for_join = None
        self._user = user
        self._is_member = None


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

    def get_is_owned(self, instance):
        return self._user.pk == instance.gathering_creator.pk if self._user is not None else None

    def get_is_available_for_join(self, instance):
        return self._user not in instance.users.all() \
               and not self._get_is_member(instance) \
               and not self._get_has_applied_for_join(instance)

    def get_has_applied_for_join(self, instance):
        return self._get_has_applied_for_join(instance)

    def get_is_member(self, instance):
        return self._get_is_member(instance)

    def _get_has_applied_for_join(self, instance):
        if self._has_applied_for_join is None:
            self._has_applied_for_join = \
                GatheringApplication.objects.filter(gathering=instance, applicant=self._user).first() is not None
        return self._has_applied_for_join

    def _get_is_member(self, instance):
        if self._is_member is None:
            self._is_member = self._user in instance.users.all()
        return self._is_member

    class Meta:
        model = Gathering
        fields = ('id', 'users', 'gathering_avatar', 'name', 'gathering_creator', 'creator', 'is_owned',
                  'is_available_for_join', 'is_member', 'has_applied_for_join')


class GatheringApplicationSerializer(serializers.ModelSerializer):
    profile_info = SerializerMethodField(read_only=True, required=False)

    def create(self, validated_data):
        app = GatheringApplication.objects.create(**validated_data)
        return app

    def get_profile_info(self, instance):
        return ProfileMedSerializer(instance.applicant).data

    class Meta:
        model = GatheringApplication
        fields = ('id', 'applicant', 'gathering', 'profile_info')
        read_only_fields = ('id', 'profile_info')


class GatheringMinSerializer(serializers.ModelSerializer):
    is_owned = SerializerMethodField()

    def __init__(self, user, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user = user

    def get_is_owned(self, instance):
        return self.user.pk == instance.gathering_creator.pk

    class Meta:
        model = Gathering
        fields = ('id', 'gathering_avatar', 'name', 'is_owned')
