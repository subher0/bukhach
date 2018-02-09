from rest_framework import viewsets
from bukhach.serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer