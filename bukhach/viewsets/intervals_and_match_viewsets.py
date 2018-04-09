from collections import defaultdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bukhach.models.interval_models import UserInterval
from django.db.models import Q

from bukhach.serializers.intervals_and_match_serializers import IntervalSerializer
from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime, IntervalAsDatetimeSerializer


class IntervalView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer_class = IntervalSerializer(data=request.data)
        if serializer_class.is_valid():
            interval = serializer_class.save()
            if interval:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)


class MatchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        intervals = UserInterval.objects.filter(~Q(user=request.user))
        currentUserIntervals = UserInterval.objects.filter(user=request.user)

        usersToIntervals = defaultdict(list)
        for interval in intervals:
            usersToIntervals[interval.user].append(interval)

        matcher = UsersToInterval()
        for currentInterval in currentUserIntervals:
            matcher.add_interval(currentInterval.start_date.timestamp(), currentInterval.end_date.timestamp())

        matcher.matchIntervals()

        for key, value in usersToIntervals.items():
            for userInterval in value:
                matcher.add_interval(userInterval.start_date.timestamp(), userInterval.end_date.timestamp())
            matcher.matchIntervals()
            matcher.add_user(key)

        matchedUsers, matchedIntervals = matcher.get_matched_intervals()

        matchedIntervalsAsTimestamps = []
        for interval in matchedIntervals:
            matchedIntervalsAsTimestamps.append(
                IntervalAsDatetimeSerializer(IntervalAsDatetime(interval['start'], interval['end'])).data)

        context = {
            'intervals': matchedIntervalsAsTimestamps,
            'users': matchedUsers
        }
        return Response(context)