from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.serializers.user_serializers import SelfProfileSerializer, UserSerializer, MinProfileSerializer, \
    MaxProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrWriteOnly]
    serializer_class = SelfProfileSerializer

    def list(self, request):
        serializer = MinProfileSerializer(Profile.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        :param request: data = {"info":"","tel_num":"88888888888", "user":{"username":"putin","password": "putin","first_name":"Владимир","last_name":"Путин"}}
        :return: user data
        """
        serializer_class = SelfProfileSerializer(data=request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            if user:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User.objects.all(), pk=pk)
        if user == request.user:
            serializer = SelfProfileSerializer(user.profile)
        else:
            serializer = MaxProfileSerializer(user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class ProfileSearchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        name = request.GET.get('name')
        if name == '':
            return Response('gay')
        else:
            words = name.split()
            if len(words) == 1:
                name = words[0]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)))
                serialized = MinProfileSerializer(profiles, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter(first_name__icontains=f_name, last_name__icontains=l_name))
                serialized = MinProfileSerializer(profiles, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
