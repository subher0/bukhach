from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile


class FullUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class FullProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = FullUserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        validated_data['user'] = User.objects.create(**user_data)
        profile = Profile.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = ('info', 'tel_num', 'avatar', 'rating', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('info', 'avatar', 'user')
