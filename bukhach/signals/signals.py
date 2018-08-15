from django.db.models.signals import post_save
from django.dispatch import receiver

from bukhach.models.interval_models import UserInterval, GatheringInterval
from bukhach.utils.matcher_utils import match


@receiver(post_save, sender=UserInterval)
def gathering_matching(sender, instance, **kwargs):
    if instance.gathering:
        GatheringInterval.objects.filter(gathering=instance.gathering).delete()
        intervals = match(instance.gathering_id)
        for interval in intervals:
            GatheringInterval.objects.create(gathering=instance.gathering, **interval)
