
import random
import os
from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator



# --------------------------------------------------
# Select a random default avatar for new users
# This function returns one avatar path randomly
# from the predefined default avatar list.
# --------------------------------------------------
def random_default_avatar():
    avatars = [
        "avatars/defaults/avatar1.png",
        "avatars/defaults/avatar2.png",
        "avatars/defaults/avatar3.png",
        "avatars/defaults/avatar4.png",
        "avatars/defaults/avatar5.png",
        "avatars/defaults/avatar6.png",
        "avatars/defaults/avatar7.png",
        "avatars/defaults/avatar8.png",
        "avatars/defaults/avatar9.png",
        "avatars/defaults/avatar10.png",
    ]
    return random.choice(avatars)


# --------------------------------------------------
# Validate the dimensions of uploaded images.
# Ensures that the width and height do not exceed
# the maximum allowed resolution (1024x1024).
# --------------------------------------------------
def validate_image_dimensions(image):
    with Image.open(image) as img:
        width, height = img.size

    if width > 1024 or height > 1024:
        raise ValidationError("Image dimensions must be under 1024x1024.")


# --------------------------------------------------
# Generate a dynamic upload path for user avatars.
# The avatar will be stored in a folder based on
# the user's username.
#
# Example:
# avatars/users/mohammad/avatar.png
# --------------------------------------------------
def user_avatar_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return f"avatars/users/{instance.username}/avatar{ext}"


# --------------------------------------------------
# Validate the file size of uploaded images.
# The maximum allowed size is 500KB.
# --------------------------------------------------
def validate_image_size(image):
    max_size = 500 * 1024
    if image.size > max_size:
        raise ValidationError("Image size must be less than 500KB.")

# --------------------------------------------------
# Custom User model extending Django's AbstractUser.
# Adds additional profile-related fields and
# avatar management features.
# --------------------------------------------------
class User(AbstractUser):


    # Optional phone number field
    # Indexed for faster lookup and unique across users
    phone = models.CharField(max_length=20, blank=True, unique=True, db_index=True, null=True)
    

    # User avatar with:
    # - custom upload path
    # - random default avatar
    # - size validation
    # - dimension validation
    # - extension validation
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        default=random_default_avatar,
        validators=[
                validate_image_size,
                validate_image_dimensions,
                FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])])

    
    # Additional profile fields
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Timestamp fields for tracking user creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the user
    def __str__(self):
        return self.username

    # --------------------------------------------------
    # Override save method to automatically delete
    # the previous avatar file when a new one is uploaded.
    #
    # This prevents unused files (orphan files) from
    # accumulating in the media storage.
    # -------------------------------------------------- 
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_user = User.objects.get(pk=self.pk)
                
                if (old_user.avatar
                    and 'defaults' not in old_user.avatar.name
                    and old_user.avatar != self.avatar):
                    
                    
                    
                    old_user.avatar.delete(save=False)
            except User.DoesNotExist:
                pass

        super().save(*args, **kwargs)


    # --------------------------------------------------
    # Model metadata configuration
    # Orders users by newest first
    # --------------------------------------------------
    class Meta:

        ordering = ['-created_at']
