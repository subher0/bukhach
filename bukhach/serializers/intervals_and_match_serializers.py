from django.utils import timezone
from rest_framework import serializers

from bukhach.models.interval_models import UserInterval, transform_time, GatheringInterval


class IntervalSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        start = transform_time(attrs['start_date'])
        end = transform_time(attrs['end_date'])
        if start >= end:
            raise serializers.ValidationError('End date must be after start date.')

        for interval in UserInterval.objects.filter(user=attrs['user'], gathering=attrs['gathering']):
            if start <= timezone.localtime(interval.start_date) <= end or \
                    start <= timezone.localtime(interval.end_date) <= end or \
                    (timezone.localtime(interval.start_date) <= start and timezone.localtime(interval.end_date) >= end):
                raise serializers.ValidationError('Interval should not intersects or concur with existing intervals')
        attrs['start_date'] = start
        attrs['end_date'] = end
        return attrs

    class Meta:
        model = UserInterval
        fields = ('id', 'user', 'start_date', 'end_date', 'gathering')
        write_only_fields = ('user',)


class GatheringIntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatheringInterval
        fields = ('start_date', 'end_date')
