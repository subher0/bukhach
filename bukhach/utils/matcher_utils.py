import datetime
import numpy

from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import DateTimeField

from bukhach.models.gathering_models import Gathering
from bukhach.models.interval_models import UserInterval
from bukhach.models.profile_models import Profile
from bukhach.serializers.user_serializers import ProfileMinSerializer


# class UsersToInterval:
#     def __init__(self):
#         self.users = []
#         self.intervals = []
#         self.alreadyMatched = []
#
#     # adds user that was participating in the match
#     def add_user(self, user):
#         if user is not None:
#             self.users.append(ProfileMinSerializer(user.profile).data)
#
#     # accumalates intervals for the next match step
#     def add_interval(self, start, end):
#         interval = {'start': start, 'end': end}
#         self.intervals.append(interval)
#
#     def matchStillPossible(self):
#         if len(self.users) == 0:
#             return True
#
#         if len(self.alreadyMatched) == 0:
#             return False
#
#     # matches added intervals with those that are already matched and rewrites alreadyMatched
#     # to the common matched intervals. If none were matched yet, intervals are simply copied to alreadyMatched
#     def matchIntervals(self):
#         if len(self.alreadyMatched) == 0 and len(self.users) == 0:
#             self.alreadyMatched = self.intervals[:]
#             self.intervals = []
#             return
#
#         newlyMatched = []
#
#         for matched in self.alreadyMatched:
#             for interval in self.intervals:
#                 if interval['start'] >= interval['end']:
#                     continue
#
#                 if interval['start'] <= matched['start'] <= interval['end'] <= matched['end']:
#                     newlyMatched.append({'start': matched['start'], 'end': interval['end']})
#                     continue
#
#                 if matched['start'] <= interval['start'] <= matched['end'] and matched['end'] >= interval['end']:
#                     newlyMatched.append({'start': interval['start'], 'end': interval['end']})
#                     continue
#
#                 if matched['start'] <= interval['start'] <= matched['end'] <= interval['end']:
#                     newlyMatched.append({'start': interval['start'], 'end': matched['end']})
#                     continue
#
#                 if interval['start'] <= matched['start'] and interval['end'] >= matched['end']:
#                     newlyMatched.append({'start': matched['start'], 'end': matched['end']})
#                     continue
#
#         self.intervals = []
#         self.alreadyMatched = newlyMatched[:]
#
#     def get_matched_intervals(self):
#         return self.users, self.alreadyMatched
#
#
# class IntervalAsDatetimeSerializer(serializers.Serializer):
#     start = DateTimeField()
#     end = DateTimeField()
#
#
# class IntervalAsDatetime:
#     def __init__(self, start, end):
#         self.start = datetime.datetime.fromtimestamp(start)
#         self.end = datetime.datetime.fromtimestamp(end)


def transform_time(dt):
    if dt.minute < 30:
        dt.replace(hour=dt.hour + datetime.timedelta(hours=1))
    dt.replace(minute=0, second=0)
    return dt


def intervals_to_array(intervals):
    """
    Transform datedime interval to binary array
    :param intervals: list of datetimes
    :return: binary array
    """
    array = numpy.array([])
    for i in range(1, len(intervals)):
        interval_in_hours = int((intervals[i] - intervals[i - 1]).total_seconds() / 3600)
        array = numpy.append(array, [1 if i % 2 == 0 else 0 for x in range(interval_in_hours)])
    return array


def match(gath_pk=None, user=None):
    """
    Matches user's inteervals
    Working only for 30 days period (starting today)
    :param gath_pk: gathering id if matching in gathering else None
    :param user: user object if matching in users's friends
    :return: list of intervals or empty list
    """
    start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    stop = start + datetime.timedelta(days=30)
    b = numpy.zeros(720, int)
    if gath_pk:
        users = Gathering.objects.get(pk=gath_pk).users.all()
    elif user:
        users = user.friends.all()
    else:
        raise ValueError('gay')

    for user in users:
        intervals = [start]
        objs = UserInterval.objects.filter(gathering_id=gath_pk, user=user, start_date__lte=stop,
                                           end_date__gt=start).order_by('start_date')
        for obj in objs:
            start_date = obj.start_date
            if start_date < start:
                start_date = start
            end_date = obj.end_date
            if end_date > stop:
                end_date = stop
            intervals = intervals + [start_date, end_date]
        intervals.append(stop)
        a = intervals_to_array(intervals)
        b = b + a

    if b.max() < users.count():
        return []

    return array_to_intervals(b, users.count(), start)


def array_to_intervals(array, count, start):
    """
    Transform array to intervals
    :param array: array of ints where int - number of matches
    :param count: int. Count of matches which will fall into interval
    :param start: start datetime
    :return: list of intervals
    """
    interval_list = []
    prev = 0
    seq = False
    for i in range(len(array) - 1):
        if array[i] == count:
            if prev == count:
                seq = True
            else:
                interval_list.append({'start_date': timezone.localtime(start + datetime.timedelta(hours=i))})
        else:
            if prev == count:
                if seq:
                    interval_list[-1]['end_date'] = timezone.localtime(start + datetime.timedelta(hours=i))
                else:
                    interval_list.pop()
            seq = False
        prev = array[i]
    if interval_list:
        if array[-1] == count:
            if seq or prev == count:
                interval_list[-1]['end_date'] = timezone.localtime(start + datetime.timedelta(hours=(i + 1)))
            else:
                interval_list.pop()
    return interval_list
