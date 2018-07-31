from collections import defaultdict

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bukhach.models.interval_models import UserInterval, GatheringInterval
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


@api_view(['GET'])
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

    GatheringInterval.objects.filter(gathering_id=gathering_id).delete()

    for interval in matchedIntervals:
        GatheringInterval.objects.create(start_matched_date=interval['start'], end_matched_date=interval['end'],
                                         gathering_id=gathering_id)

    return {
        'matchedUsers': matchedUsers,
        'matchedIntervals': matchedIntervals
    }
