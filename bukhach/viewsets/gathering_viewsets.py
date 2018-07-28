import json
from collections import defaultdict

import redis
import os
import requests
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from bukhach.consts import GatheringMessages, MainMessages
from bukhach.models.gathering_models import Gathering
from bukhach.serializers.gathering_serializers import GatheringMaxSerializer, GatheringMinSerializer, \
    GatheringApplicationSerializer


class GatheringViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        Create gathering
        :param request: data = {"gathering_avatar": "ava", "name": "name"}
        :return: gathering data
        """
        data = request.data
        data['creator'] = request.user.profile.id
        serializer_class = GatheringMaxSerializer(data=data)
        if serializer_class.is_valid():
            gathering = serializer_class.save()
            if gathering:
                return Response(GatheringMaxSerializer(gathering).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)

    def update(self, request, pk=None):
        """
        Update gathering. Only name and gathering_avatar update allowed
        :param request: data = {**kwargs}
        :return: gathering data
        """
        if 'users' in request.data:
            del request.data['users']
        if 'gathering_creator' in request.data:
            del request.data['gathering_creator']
        try:
            gathering = Gathering.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator != request.user.profile:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)
        serializer_class = GatheringMaxSerializer(gathering, request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(GatheringMaxSerializer(Gathering.objects.get(pk=pk)).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        gathering = get_object_or_404(Gathering.objects.all(), pk=pk)
        if request.user.profile == gathering.gathering_creator:
            serializer = GatheringMaxSerializer(gathering)
        else:
            serializer = GatheringMinSerializer(gathering)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Get list of self gatherings
        :param request:
        """
        return Response(GatheringMinSerializer(request.user.profile.gatherings, many=True).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Delete Gathering
        """
        gathering = get_object_or_404(Gathering.objects.all(), pk=pk)
        if request.user.profile == gathering.gathering_creator:
            gathering.delete()
            return Response({'message': 'GAY DELETE'}, status=status.HTTP_200_OK)
        else:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)


class GatheringApplicationViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, gathering_pk=None):
        """

        :param request: data = {"gathering_id"}
        :return:
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.users.filter(id=request.user.profile.id):
            return Response(GatheringMessages.ALREADY_EXIST, status=status.HTTP_400_BAD_REQUEST)
        if gathering.applications.filter(applicant=request.user.profile):
            return Response({'message': 'Тебе же сказали - не лезь блядь она тебя сожрет'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['applicant'] = request.user.profile.id
        request.data['gathering'] = gathering_pk
        serializer_class = GatheringApplicationSerializer(data=request.data)
        if serializer_class.is_valid():
            application_id = serializer_class.save()
            return Response({'application_id': application_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, gathering_pk=None):
        """
        List of all applications of user`s gathering
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator != request.user.profile:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status.HTTP_403_FORBIDDEN)
        return Response(GatheringApplicationSerializer(gathering.applications, many=True).data, status=status.HTTP_200_OK)

    def retrieve(self, request, gathering_pk=None, pk=None):
        """
        Get application info
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator != request.user.profile:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)
        try:
            application = gathering.applications.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        return Response(GatheringApplicationSerializer(application).data, status=status.HTTP_200_OK)

    def destroy(self, request, gathering_pk=None, pk=None):
        """
        Reject or cancel application
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        try:
            app = gathering.applications.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator == request.user.profile or app.applicant == request.user.profile:
            app.delete()
            return Response(MainMessages.OK, status=status.HTTP_200_OK)
        else:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, gathering_pk=None, pk=None):
        """
        Apply application
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator != request.user.profile:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)
        try:
            app = gathering.applications.get(pk=pk)
            applicant = app.applicant
            gathering.users.add(applicant)
            app.delete()
            return Response(GatheringMaxSerializer(gathering).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)


class GatheringSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        name = request.GET.get('name', None)
        if not name:
            return Response(GatheringMessages.UNSUPPORTED_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)

        gatherings = Gathering.objects.filter(name__icontains=name)
        if not gatherings:
            return Response('', status=status.HTTP_404_NOT_FOUND)
        return Response(GatheringMinSerializer(gatherings, many=True), status=status.HTTP_200_OK)
