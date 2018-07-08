from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from bukhach.models.profile_models import Profile
from bukhach.serializers.friends_serializer import FriendsSerializer, FriendFullSerializer

FRIEND_EXISTS_MESSAGE = {'message': 'This one is already in your friends list'}
FRIEND_DOES_NOT_EXIST_MESSAGE = {'message': 'This one is not in your friends list'}
PROFILE_DOES_NOT_EXIST_MESSAGE = {'message': 'The man you are trying to add doesn\'t seem to exist'}
FRIEND_ADDED_MESSAGE = {'message': 'You are now friends with this man'}
FRIEND_DELETED_MESSAGE = {'message': 'You are no longer friends with this man'}


class FriendsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    # Retrieves All friends of current user
    def list(self, request):
        friends = Profile.objects.filter(user=request.user).first().friends.all()
        friendsResponse = []
        for friend in friends:
            friendsResponse.append(FriendsSerializer(friend).data)
        return Response(friendsResponse)

    #Retrieves fuller data of a friend which primary key equals to pk
    def retrieve(self, request, pk=None):
        profile = Profile.objects.filter(user=request.user).first()
        friend = Profile.objects.filter(pk=pk).first()
        if friend is None:
            return Response(data=PROFILE_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        if not profile.friends.filter(pk=pk).exists():
            return Response(data=FRIEND_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        return Response(FriendFullSerializer(friend).data)

    # Adds profile which primary key equals to pk to current profile's friends list
    def update(self, request, pk=None):
        profile = Profile.objects.filter(user=request.user).first()
        friend = Profile.objects.filter(pk=pk).first()
        if friend is None:
            return Response(data=PROFILE_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        if profile.friends.filter(pk=pk).exists():
            return Response(data=FRIEND_EXISTS_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        profile.friends.add(friend)
        return Response(data=FRIEND_ADDED_MESSAGE, status=status.HTTP_202_ACCEPTED)

    # Deletes profile which primary key equals to pk from current profile's friends list
    def destroy(self, request, pk=None):
        profile = Profile.objects.filter(user=request.user).first()
        friend = Profile.objects.filter(pk=pk).first()
        if friend is None:
            return Response(data=PROFILE_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        if not profile.friends.filter(pk=pk).exists():
            return Response(data=FRIEND_DOES_NOT_EXIST_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        profile.friends.remove(friend)
        return Response(data=FRIEND_DELETED_MESSAGE, status=status.HTTP_204_NO_CONTENT)
