import datetime
from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from bukhach.consts import IntervalMessages, GatheringMessages, MainMessages
from bukhach.models.gathering_models import Gathering
from bukhach.models.interval_models import UserInterval, GatheringInterval
from django.db.models import Q

from bukhach.serializers.intervals_and_match_serializers import IntervalSerializer
from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime, IntervalAsDatetimeSerializer


class IntervalViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, gathering_pk=None):
        try:
            if not self._is_interval_valid(request.data,
                                           UserInterval.objects.get(user=request.user.profile, gathering__pk=gathering_pk)):
                return Response(IntervalMessages.INTERVAL_INVALID, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        try:
            gathering = Gathering.objects.get(pk=gathering_pk, users=request.user.profile)
        except ObjectDoesNotExist:
            return Response(GatheringMessages.WTF_GAY_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = request.user.profile.id
        request.data['gathering'] = gathering.id
        serializer_class = IntervalSerializer(data=request.data)
        if serializer_class.is_valid():
            interval = serializer_class.save()
            if interval:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)

    def list(self, request, gathering_pk=None):
        intervals = UserInterval.objects.filter(user=request.user.profile, gathering__pk=gathering_pk)
        return Response(IntervalSerializer(intervals, many=True).data)

    def destroy(self, request, gathering_pk=None, pk=None):
        try:
            interval = UserInterval.objects.get(pk=pk, user=request.user, gathering__pk=gathering_pk)
        except ObjectDoesNotExist:
            return Response(IntervalMessages.INTERVAL_INVALID)
        interval.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def match(self, request, gathering_pk):
        """
        Extremely temporary. Replace it with normal code as soon as you get a chance
        :param request:
        :param gathering_pk:
        :return:
        """
        return get_matches(request, gathering_pk)

    def _is_interval_valid(self, interval, previous_intervals):
        return True

def get_matches(request, gathering_id):
    return Response(perform_match(request, gathering_id))


def perform_match(request, gathering_id):
    intervals = UserInterval.objects.filter(gathering_id=gathering_id)

    usersToIntervals = defaultdict(list)
    for interval in intervals:
        usersToIntervals[interval.user].append(interval)

    matcher = UsersToInterval()

    for key, value in usersToIntervals.items():
        for userInterval in value:
            matcher.add_interval(userInterval.start_date.timestamp(), userInterval.end_date.timestamp())
        matcher.matchIntervals()
        matcher.add_user(key)

    matchedUsers, matchedIntervals = matcher.get_matched_intervals()

    matched_intervals_foramatted = []
    for interval in matchedIntervals:
        formatted_interval = {}
        formatted_interval['start_date'] = datetime.datetime.fromtimestamp(interval['start'])
        formatted_interval['end_date'] = datetime.datetime.fromtimestamp(interval['end'])
        matched_intervals_foramatted.append(formatted_interval)

    # GatheringInterval.objects.filter(gathering_id=gathering_id).delete()
    #
    # for interval in matchedIntervals:
    #     GatheringInterval.objects.create(start_matched_date=interval['start'], end_matched_date=interval['end'],
    #                                      gathering_id=gathering_id)

    return matched_intervals_foramatted
