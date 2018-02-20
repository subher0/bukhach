from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bukhach.serializers import UserSerializer, GroupSerializer, ProfileSerializer
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request):
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


class ProfileSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def __info_append(users, content):
        for user in users:
            element = {'first_name': user.first_name,
                       'last_name': user.last_name,
                       'username': user.username,
                       'email': user.email,
                       'info': user.profile.info,
                       'tel_num': user.profile.tel_num,
                       'rating': user.profile.rating,
                       'avatar': str(user.profile.avatar)
                       }
            content.append(element)
        return content

    def get(self,request):
        content = []
        name = request.GET.get('name')
        if name == '':
            return Response('gay')
        else:
            words = name.split()
            if len(words) == 1:
                name = words[0]
                users = User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
                response = Response(self.__info_append(users, content))
                return response
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                users = User.objects.filter(first_name__icontains=f_name, last_name__icontains=l_name)
                response = Response(self.__info_append(users, content))
                return response
