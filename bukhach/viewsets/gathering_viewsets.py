from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from bukhach.consts import GatheringMessages
from bukhach.models.gathering_models import Gathering
from bukhach.serializers.gathering_serializers import GatheringMaxSerializer, GatheringMinSerializer, \
    GatheringApplicationSerializer


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
        serializer_class = GatheringMaxSerializer(gathering, request.data, user=request.user.profile, partial=True)
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
            serializer = GatheringMaxSerializer(gathering, user=request.user.profile)
        else:
            serializer = GatheringMaxSerializer(gathering, user=request.user.profile,)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Get list of self gatherings
        :param request:
        """
        response = GatheringMinSerializer(request.user.profile,
                                        request.user.profile.gatherings, many=True)

        response.is_valid()
        return Response(response.data, status=status.HTTP_200_OK)

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

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk=None):
        """
        Leave the gathering
        """
        try:
            gathering = Gathering.objects.filter(pk=pk, users=request.user.profile) \
                .exclude(gathering_creator=request.user.profile).get()
        except ObjectDoesNotExist:
            return Response(GatheringMessages.WTF_GAY_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        gathering.users.remove(request.user.profile)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def search(self, request):
        name = request.GET.get('name', None)
        if not name:
            return Response(GatheringMessages.UNSUPPORTED_SEARCH_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        gatherings = Gathering.objects.filter(name__icontains=name)
        response = GatheringMinSerializer(request.user.profile,
                                               gatherings, many=True)
        response.is_valid()
        return Response(response.data, status=status.HTTP_200_OK)


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
        request.data['gathering'] = gathering.id
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

    def delete(self, request, gathering_pk=None):
        """
        Withdraw application (for currently authenticated user)
        """
        try:
            gathering = Gathering.objects.get(pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.GATHERING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        try:
            app = gathering.applications.get(applicant=request.user.profile)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.APPLICATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if gathering.gathering_creator == request.user.profile or app.applicant == request.user.profile:
            app.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(GatheringMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, gathering_pk=None, pk=None):
        """
        Reject user's application (for group admin)
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
            return Response(status=status.HTTP_204_NO_CONTENT)
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
