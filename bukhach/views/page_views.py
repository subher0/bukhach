from collections import defaultdict
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader

from bukhach.models.matcher_models import UserInterval
from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime

from bukhach.models.profile_models import Profile


def index_view(request):
    template = loader.get_template('bukhach/index.html')
    context = {
        "ip": request.META['HTTP_X_REAL_IP']
    }
    return HttpResponse(template.render(context, request))


def about_us_view(request):
    template = loader.get_template('bukhach/about_us.html')
    context = {}
    return HttpResponse(template.render(context, request))


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


def contacts_view(request):
    template = loader.get_template('bukhach/contacts.html')
    context = {}
    return HttpResponse(template.render(context, request))