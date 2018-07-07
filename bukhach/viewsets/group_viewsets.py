import json
from collections import defaultdict

import redis
import os
import requests

from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from bukhach.models.group_models import Gathering
from bukhach.models.interval_models import UserInterval
from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.serializers.group_serializers import GatheringSerializer
from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime, IntervalAsDatetimeSerializer


class GatheringView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Create gathering
        :param request: data = {"users": ["user_id1", "user_id2"], "gathering_avatar": "ava", "name": "name"}
        :return: gathering id
        """
        data = request.data
        data['gathering_creator'] = request.user.id
        data['users'].append(request.user.id)
        serializer_class = GatheringSerializer(data=data)
        if serializer_class.is_valid():
            gathering_id = serializer_class.save()
            if gathering_id:
                return Response(json.dumps({'gathering_id': gathering_id}), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)
