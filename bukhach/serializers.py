from django.contrib.auth.models import User, Group
from rest_framework import serializers
from bukhach.models.profile_models import Profile
from bukhach.models.matcher_models import UserInterval


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'username')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        validated_data['user'] = User.objects.create(**user_data)
        profile = Profile.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = ('info', 'tel_num', 'avatar', 'rating', 'user')


class IntervalSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInterval
        fields = ('user', 'start_date', 'end_date')