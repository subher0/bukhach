from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from bukhach.models.profile_models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'username')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'username')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        validated_data['user'] = User.objects.create(**user_data)
        profile = Profile.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = ('user', 'info', 'tel_num', 'avatar', 'rating')
