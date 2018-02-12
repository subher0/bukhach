from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bukhach.serializers import UserSerializer, GroupSerializer, ProfileSerializer
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
        profile = Profile.objects.filter(user = request.user).first()
        response = Response({'first_name': profile.user.first_name})
        response['Access-Control-Allow-Origin'] = 'http://176.112.233.43:3000'
        return response
