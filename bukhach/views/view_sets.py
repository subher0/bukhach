from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from bukhach.serializers import UserSerializer, GroupSerializer, RegisterUser
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile


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


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer_class = RegisterUser(data=request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            if user:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)