from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from bukhach.models.interval_models import UserInterval
from bukhach.serializers.intervals_and_match_serializers import IntervalSerializer
from bukhach.consts import IntervalMessages
from bukhach.utils.matcher_utils import match


class IntervalViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        :param request:
        {
            "start_date": "2018-09-08T12:00:00+03:00",
            "end_date": "2018-11-08T12:00:00+03:00",
            "gathering": 1
        }
        :return: interval info
        """
        request.data['user'] = request.user.profile.id
        serializer = IntervalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        :return: user's intervals
        """
        return Response(IntervalSerializer(UserInterval.objects.filter(user=request.user.profile.id), many=True).data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        :param pk: gathering pk
        :return: user's gathering intervals or user's free intervals(pk=0)
        """
        if pk == 0:
            pk = None
        return Response(
            IntervalSerializer(UserInterval.objects.filter(user=request.user.profile, gathering_id=pk),
                               many=True).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            UserInterval.objects.get(user=request.user.profile, pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserInterval.DoesNotExist:
            return Response(IntervalMessages.INTERVAL_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            interval = UserInterval.objects.get(user=request.user.profile, pk=pk)
        except UserInterval.DoesNotExist:
            return Response(IntervalMessages.INTERVAL_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
        request.data.pop('user')
        request.data.pop('gathering')
        serializer = IntervalSerializer(interval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def match(self, request):
        """
        Matches free intervals by user and user's friens
        :return: interval list
        """
        return Response(match(user=request.user.profile), status=status.HTTP_200_OK)
