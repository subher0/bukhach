from rest_framework import serializers

from bukhach.models.interval_models import UserInterval


class IntervalSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user_interval = UserInterval.objects.create(**validated_data)
        return user_interval

    class Meta:
        model = UserInterval
        fields = ('id', 'user', 'start_date', 'end_date', 'gathering')
        read_only_fields = ('id',)