from collections import defaultdict
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from bukhach.models.profile_models import Profile
from bukhach.models.matcher_models import UserInterval
from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime
from rest_framework import viewsets
from bukhach.serializers import UserSerializer, GroupSerializer


def index_view(request):
    template = loader.get_template('bukhach/index.html')
    profiles = Profile.objects.order_by('-rating', 'user__username')[:5]
    context = {
        'profiles': profiles
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def match_view(request):
    template = loader.get_template('bukhach/match.html')
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
        matchedIntervalsAsTimestamps.append(IntervalAsDatetime(interval['start'], interval['end']))

    context = {
        'intervals': matchedIntervalsAsTimestamps,
        'users': matchedUsers
    }
    return HttpResponse(template.render(context, request))


def gay_view(request):
    template = loader.get_template('bukhach/GAY.html')
    context = {}
    return HttpResponse(template.render(context, request))


def fuck_yourself_view(request):
    template = loader.get_template('bukhach/GTFO/fuck_yourself.html')
    context = {}
    return HttpResponse(template.render(context, request))


def appeals_view(request):
    template = loader.get_template('bukhach/appeals.html')
    context = {}
    return HttpResponse(template.render(context, request))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer