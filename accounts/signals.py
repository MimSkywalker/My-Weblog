# --------------------------------------------------
# Django Signals for the User model
# This signal automatically deletes the user's avatar
# file from storage when the user object itself is deleted.
# --------------------------------------------------

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import User


# --------------------------------------------------
# post_delete signal:
# Runs *after* a User instance is deleted from the database.
#
# Purpose:
# Prevent orphaned files in MEDIA_ROOT by manually deleting
# the user's avatar file from the filesystem/storage.
# --------------------------------------------------
@receiver(post_delete, sender=User)
def delete_user_avatar(sender, instance, **kwargs):
    """
    Deletes the avatar file from storage after the User object is deleted.
    """

    # --------------------------------------------------
    # Conditions:
    # 1. instance.avatar must exist (user has an avatar)
    # 2. Avatar name must not contain "defaults"
    #    This prevents deleting the default avatar image,
    #    which is shared among all users.
    # --------------------------------------------------
    if instance.avatar and "defaults" not in instance.avatar.name:

        # Delete the file from storage (filesystem or S3)
        # save=False → prevents Django from updating the model again
        instance.avatar.delete(save=False)
