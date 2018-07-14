import json
from collections import defaultdict

import redis
import os
import requests

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
#from rest_framework.decorators import

from bukhach.models.gathering_models import Gathering
from bukhach.models.interval_models import UserInterval
from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.serializers.group_serializers import GatheringCreateSerializer, \
    GatheringFullGetSerializer, GatheringUpdateSerializer, GatheringMinGetSerializer
from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime, IntervalAsDatetimeSerializer


class GatheringViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        Create gathering
        :param request: data = {"gathering_avatar": "ava", "name": "name"}
        :return: gathering id
        """
        data = request.data
        data['gathering_creator'] = request.user.profile.id
        data['users'] = [request.user.profile.id]
        serializer_class = GatheringCreateSerializer(data=data)
        if serializer_class.is_valid():
            gathering_id = serializer_class.save()
            if gathering_id:
                return Response({'gathering_id': gathering_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)

    def update(self, request, pk=None):
        """
        Update gathering. Only name and gathering_avatar update allowed
        :param request: data = {**kwargs}
        :return: gathering data
        """
        queryset = Gathering.objects.all()
        serializer_class = GatheringUpdateSerializer(get_object_or_404(queryset, pk=pk), request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            serializer_class = GatheringFullGetSerializer(Gathering.objects.get(pk=pk))
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors)

    def retrieve(self, request, pk=None):
        queryset = Gathering.objects.all()
        gathering = get_object_or_404(queryset, pk=pk)
        if request.user.profile == gathering.gathering_creator:
            serializer = GatheringFullGetSerializer(gathering)
        else:
            serializer = GatheringMinGetSerializer(gathering)
        return Response(serializer.data)

    def list(self, request):
        serializer_class = GatheringMinGetSerializer(Gathering.objects.all(), many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        gathering = get_object_or_404(Gathering.objects.all(), pk=pk)
        if request.user.profile == gathering.gathering_creator:
            gathering.delete()
            return Response({'message': 'Delete'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You don\'t have permissions to delete this gathering'}, status=status.HTTP_403_FORBIDDEN)


class GatheringApplicationViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """

        :param request: data = {"gathering_id"}
        :return:
        """
        pass
