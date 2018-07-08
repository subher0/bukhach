from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.serializers.friends_serializer import FriendsSerializer
from bukhach.serializers.user_serializers import FullProfileSerializer, FullUserSerializer, ProfileSerializer

UNSUPPORTED_SEARCH_MESAGE = {'message': 'The saerch text is unsupported. Only one or two words text is supported for now'}
EMPTY_SEARCH_MESAGE = {'message': 'You requested search by empty text'}

PROFILE_DOES_NOT_EXIST = {'message': 'Requested profile does not exist'}

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FullUserSerializer


class ProfileViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    serializer_class = FullProfileSerializer

    def list(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        print(profile.avatar)
        print(profile.user.first_name)
        response = Response({'first_name': profile.user.first_name,
                             'last_name': profile.user.last_name,
                             'username': profile.user.username,
                             'email': profile.user.email,
                             'info': profile.info,
                             'tel_num': profile.tel_num,
                             'rating': profile.rating,
                             'avatar': str(profile.avatar)
                             })
        return response

    def retrieve(self, request, pk=None):
        profile = Profile.objects.filter(pk=pk).first()
        if profile is None:
            return Response(data=PROFILE_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
        response = ProfileSerializer(profile).data
        return Response(response)

    def post(self, request, *args, **kwargs):
        serializer_class = FullProfileSerializer(data=request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            if user:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)


class ProfileSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def __info_append(users, content):
        for user in users:
            element = FriendsSerializer(user.profile).data
            content.append(element)
        return content

    def get(self, request):
        content = []
        name = request.GET.get('name')
        if name == '':
            return Response(data=EMPTY_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)
        else:
            words = name.split()
            if len(words) == 1:
                name = words[0]
                users = User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)
                                            | Q(username__icontains=name))
                response = Response(self.__info_append(users, content))
                return response
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                users = User.objects.filter(Q(first_name__icontains=f_name, last_name__icontains=l_name)
                                            | Q(last_name__icontains=f_name, first_name__icontains=l_name))
                response = Response(self.__info_append(users, content))
                return response
        return Response(data=UNSUPPORTED_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)