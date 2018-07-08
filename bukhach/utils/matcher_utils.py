import datetime

from rest_framework import serializers
from rest_framework.fields import DateTimeField

from bukhach.serializers.user_serializers import FullProfileSerializer


class UsersToInterval:
    def __init__(self):
        self.users = []
        self.intervals = []
        self.alreadyMatched = []

    # adds user that was participating in the match
    def add_user(self, user):
        if user is not None:
            self.users.append(FullProfileSerializer(user.profile).data)

    # accumalates intervals for the next match step
    def add_interval(self, start, end):
        interval = {'start': start, 'end': end}
        self.intervals.append(interval)

    def matchStillPossible(self):
        if len(self.users) == 0:
            return True

        if len(self.alreadyMatched) == 0:
            return False

    # matches added intervals with those that are already matched and rewrites alreadyMatched
    # to the common matched intervals. if none were matched yet, intervals are copied to alreadyMatched
    def matchIntervals(self):
        if len(self.alreadyMatched) == 0 and len(self.users) == 0:
            self.alreadyMatched = self.intervals[:]
            self.intervals = []
            return

        newlyMatched = []

        for matched in self.alreadyMatched:
            for interval in self.intervals:
                if interval['start'] >= interval['end']:
                    continue

                if interval['start'] <= matched['start'] <= interval['end'] <= matched['end']:
                    newlyMatched.append({'start': matched['start'], 'end': interval['end']})
                    continue

                if matched['start'] <= interval['start'] <= matched['end'] and matched['end'] >= interval['end']:
                    newlyMatched.append({'start': interval['start'], 'end': interval['end']})
                    continue

                if matched['start'] <= interval['start'] <= matched['end'] <= interval['end']:
                    newlyMatched.append({'start': interval['start'], 'end': matched['end']})
                    continue

                if interval['start'] <= matched['start'] and interval['end'] >= matched['end']:
                    newlyMatched.append({'start': matched['start'], 'end': matched['end']})
                    continue

        self.intervals = []
        self.alreadyMatched = newlyMatched[:]

    def get_matched_intervals(self):
        return self.users, self.alreadyMatched


class IntervalAsDatetimeSerializer(serializers.Serializer):
    start = DateTimeField()
    end = DateTimeField()


class IntervalAsDatetime:
    def __init__(self, start, end):
        self.start = datetime.datetime.fromtimestamp(start)
        self.end = datetime.datetime.fromtimestamp(end)
