import os

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from bukhach.models.profile_models import Profile


@receiver(post_delete, sender=Profile)
def auto_delete_file_and_user_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem and delete bound user
    when corresponding `Profile` object is deleted.
    """
    if instance.avatar and instance.avatar.path.find('def_ava') == -1:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
    instance.user.delete()


@receiver(pre_save, sender=Profile)
def auto_delete_file_on_change(instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Profile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Profile.objects.get(pk=instance.pk).avatar
    except ObjectDoesNotExist:
        return False

    if old_file.path.find('def_ava') != -1:
        return False

    new_file = instance.avatar
    if old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)