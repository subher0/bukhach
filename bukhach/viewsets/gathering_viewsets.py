from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from bukhach.consts import GatheringMessages
from bukhach.models.gathering_models import Gathering
from bukhach.models.interval_models import GatheringInterval
from bukhach.serializers.gathering_serializers import GatheringMaxSerializer, GatheringMinSerializer, \
    GatheringApplicationSerializer
from bukhach.serializers.intervals_and_match_serializers import GatheringIntervalSerializer


class GatheringViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        Create gathering
        :param request: data = {"name": "name"}
        :return: gathering data
        """
        data = request.data
        data['creator'] = request.user.profile.id
        serializer_class = GatheringMaxSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)

    def update(self, request, pk=None):
        """
        Update gathering. Only name and gathering_avatar update allowed
        :param request: data = {**kwargs}, avatar as file
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
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            gathering = Gathering.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
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
        try:
            gathering = Gathering.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if request.user.profile == gathering.gathering_creator:
            gathering.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=False)
    def search(self, request):
        name = request.GET.get('name', None)
        if not name:
            return Response(GatheringMessages.UNSUPPORTED_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)

        gatherings = Gathering.objects.filter(name__icontains=name)
        return Response(GatheringMinSerializer(gatherings, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def match(self, request, pk=None):
        try:
            gathering = Gathering.objects.get(pk=pk)
        except Gathering.DoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if not gathering.users.filter(user=request.user):
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)
        return Response(GatheringIntervalSerializer(GatheringInterval.objects.filter(gathering_id=pk), many=True).data, status=status.HTTP_200_OK)


class GatheringApplicationViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, gathering_pk=None):
        """
        :param gathering_pk: gath pk
        :param request: data = {"gathering_id"}
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.users.filter(id=request.user.profile.id):
            return Response(GatheringMessages.ALREADY_EXIST, status=status.HTTP_400_BAD_REQUEST)
        if gathering.applications.filter(applicant=request.user.profile):
            return Response(GatheringMessages.WTF_GAY_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        request.data['applicant'] = request.user.profile.id
        request.data['gathering'] = gathering_pk
        serializer_class = GatheringApplicationSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
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

    def retrieve(self, request, gathering_pk=None, application_pk=None):
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
            application = gathering.applications.get(pk=application_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        return Response(GatheringApplicationSerializer(application).data, status=status.HTTP_200_OK)

    def destroy(self, request, gathering_pk=None, application_pk=None):
        """
        Reject or cancel application
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        try:
            app = gathering.applications.get(pk=application_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator == request.user.profile or app.applicant == request.user.profile:
            app.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, gathering_pk=None, application_pk=None):
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
            app = gathering.applications.get(pk=application_pk)
            applicant = app.applicant
            gathering.users.add(applicant)
            app.delete()
            return Response(GatheringMaxSerializer(gathering).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
