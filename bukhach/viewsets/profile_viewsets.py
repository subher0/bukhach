from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User
from bukhach.models.profile_models import Profile
from django.db.models import Q
from bukhach.consts import ProfileMessages, MainMessages

from bukhach.serializers.user_serializers import ProfileMinSerializer, ProfileMaxSerializer, ProfileMedSerializer


class ProfileViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrWriteOnly,)

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

    def post(self, request, *args, **kwargs):
        serializer_class = ProfileMaxSerializer(data=request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            if user:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)

    # Only for debug mode
    def destroy(self, request, pk=None):
        try:
            Profile.objects.get(user=request.user).delete()
            return Response(MainMessages.OK, status=status.HTTP_200_OK)
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


class ProfileSearchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
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
                    user__in=User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)))
                serialized = ProfileMinSerializer(profiles, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter(first_name__icontains=f_name, last_name__icontains=l_name))
                serialized = ProfileMinSerializer(profiles, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
