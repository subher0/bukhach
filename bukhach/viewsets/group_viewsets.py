from collections import defaultdict

import redis
import os
import requests

from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from bukhach.models.interval_models import UserInterval
from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime, IntervalAsDatetimeSerializer


# class GatheringView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         serializer_class = GatheringSerializer(data=request.data)
#         if serializer_class.is_valid():
#             custom_group = serializer_class.save()
#             if custom_group:
#                 return Response(serializer_class.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer_class.errors)
#         return Response(serializer_class.errors)
