from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from bukhach.models.profile_models import Profile
from bukhach.serializers.user_serializers import ProfileMinSerializer, ProfileMedSerializer
from bukhach.consts import FriendMessages


class FriendsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    # Retrieves All friends of current user
    def list(self, request):
        friends = Profile.objects.get(user=request.user).friends.all()
        return Response(ProfileMinSerializer(friends, many=True).data, status=status.HTTP_200_OK)

    #Retrieves fuller data of a friend which primary key equals to pk
    def retrieve(self, request, pk=None):
        profile = Profile.objects.get(user=request.user)

        try:
            friend = Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(data=FriendMessages.PROFILE_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)

        try:
            friend = profile.friends.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(data=FriendMessages.FRIEND_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProfileMedSerializer(friend).data, status=status.HTTP_200_OK)

    # Adds profile which primary key equals to pk to current profile's friends list
    def update(self, request, pk=None):
        profile = Profile.objects.get(user=request.user)

        try:
            friend = Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(data=FriendMessages.PROFILE_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)

        if profile.friends.filter(pk=pk).exists():
            return Response(data=FriendMessages.FRIEND_EXISTS_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        profile.friends.add(friend)
        return Response(data=FriendMessages.FRIEND_ADDED_MESSAGE, status=status.HTTP_202_ACCEPTED)

    # Removes profile which primary key equals to pk from current profile's friends list
    def destroy(self, request, pk=None):
        profile = Profile.objects.get(user=request.user)

        try:
            friend = Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(data=FriendMessages.PROFILE_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)

        if not profile.friends.filter(pk=pk).exists():
            return Response(data=FriendMessages.FRIEND_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        profile.friends.remove(friend)
        return Response(data=FriendMessages.FRIEND_DELETED_MESSAGE, status=status.HTTP_204_NO_CONTENT)
