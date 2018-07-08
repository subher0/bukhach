from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils import model_meta

from bukhach.models.profile_models import Profile
from bukhach.serializers import user_serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class FriendsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def build_unknown_field(self, field_name, model_class):
        return self.build_standard_field(field_name, model_meta.get_field_info(User).fields_and_pk[field_name])

    class Meta:
        model = Profile
        fields = ('id', 'avatar', 'user')


class FriendFullSerializer(serializers.ModelSerializer):
    user = user_serializers.FullUserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'avatar', 'info', 'rating', 'user')