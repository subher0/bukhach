from django.contrib.auth.models import User
from rest_framework import serializers

from bukhach.models.profile_models import Profile


class UserMaxSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ProfileMaxSerializer(serializers.ModelSerializer):
    user = UserMaxSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_active'] = False
        validated_data['user'] = User.objects.create_user(**user_data)
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            password = user_data.pop('password', None)
            if password:
                user.set_password(password)
            User.objects.filter(id=user.id).update(**user_data)
        avatar = validated_data.pop('avatar', None)
        if avatar:
            instance.avatar = avatar
            instance.save()
        else:
            Profile.objects.filter(id=instance.id).update(**validated_data)
        return Profile.objects.get(id=instance.id)

    class Meta:
        model = Profile
        fields = ('id', 'info', 'tel_num', 'avatar', 'rating', 'user')


class ProfileMedSerializer(serializers.ModelSerializer):
    user = UserMinSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'info', 'avatar', 'rating', 'user')


class ProfileMinSerializer(serializers.ModelSerializer):
    user = UserMinSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'avatar', 'user')