from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from bukhach.consts import ProfileMessages, MainMessages
from bukhach.models.profile_models import Profile, Invite
from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from bukhach.serializers.user_serializers import ProfileMinSerializer, ProfileMaxSerializer, ProfileMedSerializer


class ProfileViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrWriteOnly,)

    def create(self, request):
        invite_code = request.data.get('invite', None)

        try:
            invite = Invite.objects.get(invitation_code=invite_code)
        except ObjectDoesNotExist:
            return Response(ProfileMessages.INVITE_DOES_NOT_EXIST, status=status.HTTP_401_UNAUTHORIZED)

        if invite.user is not None:
            return Response(ProfileMessages.INVITE_TAKEN, status=status.HTTP_401_UNAUTHORIZED)

        serializer_class = ProfileMaxSerializer(data=request.data)
        if serializer_class.is_valid():
            profile = serializer_class.save()
            invite.user = profile.user
            invite.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        profile = Profile.objects.get(user=request.user)
        response = Response(ProfileMaxSerializer(profile).data, status=status.HTTP_200_OK)
        return response

    def retrieve(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(data=ProfileMessages.PROFILE_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
        return Response(ProfileMedSerializer(profile).data, status=status.HTTP_200_OK)

    # Only for debug mode
    def destroy(self, request, pk=None):
        try:
            Profile.objects.get(user=request.user).delete()
            return Response(MainMessages.OK, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(ProfileMessages.PROFILE_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        if int(pk) != request.user.profile.id:
            return Response(ProfileMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileMaxSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def search(self, request):
        name = request.GET.get('name', None)
        if not name:
            return Response(ProfileMessages.EMPTY_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)
        name = name.strip()
        if not name:
            return Response(ProfileMessages.UNSUPPORTED_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)
        else:
            words = name.split()
            if len(words) == 1:
                name = words[0]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter(
                        Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(username__icontains=name)))
                return Response(ProfileMinSerializer(profiles, many=True).data, status=status.HTTP_200_OK)
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter((Q(first_name__icontains=f_name) & Q(last_name__icontains=l_name)) | (
                                Q(first_name__icontains=l_name) & Q(last_name__icontains=f_name)))).distinct()
                serialized = ProfileMinSerializer(profiles, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
