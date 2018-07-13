from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.serializers.user_serializers import ProfileSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrWriteOnly]
    serializer_class = ProfileSerializer

    def list(self, request):
        pass

    def create(self, request):
        """
        :param request: data = {'tel_num':'88888888888', 'user': {'username': 'imgay', 'email': 'im@g.ay',
                                                       'first_name': 'im', 'last_name': 'gay', 'password': 'gayyy'}}
        :return:
        """
        serializer_class = ProfileSerializer(data=request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            if user:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)

    def retrieve(self, request, pk=None):
        profile = User.objects.filter(pk=pk).first().profile
        response = Response({'first_name': profile.user.first_name,
                             'id': profile.user.id,
                             'last_name': profile.user.last_name,
                             'username': profile.user.username,
                             'email': profile.user.email,
                             'info': profile.info,
                             'tel_num': profile.tel_num,
                             'rating': profile.rating,
                             'avatar': str(profile.avatar)
                             })
        return response

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class ProfileSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def __info_append(users, content):
        for user in users:
            element = {'id': user.id,
                       'first_name': user.first_name,
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

    def get(self, request):
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
