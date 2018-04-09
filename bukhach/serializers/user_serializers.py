from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


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
