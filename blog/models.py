
from tkinter import CASCADE
from turtle import title
from unicodedata import category

from django.db import models

# Settings for author
from django.conf import settings

# except
from django.utils.text import Truncator
from django.utils.html import strip_tags


from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ObjectDoesNotExist

from slugify import slugify


from PIL import Image

import os
import uuid
import shutil


def validate_image_dimensions(image):
    min_width, min_height = 640, 360
    max_width, max_height = 1920, 1080

    if not image:
        return
    
    try:
        with Image.open(image) as img:
            width, height = img.size
    except Exception:
        raise ValidationError("Uploaded file is not a valid image.")

    if width < min_width or height < min_height:
        raise ValidationError(
            f"Image is too small. Minimum size is {min_width}x{min_height} pixels."
        )

    if width > max_width or height > max_height:
        raise ValidationError(
            f"Image is too large. Maximum size is {max_width}x{max_height} pixels."
        )




def post_featured_image_avatar_path(instance, filename):
    _, ext = os.path.splitext(filename)

    if instance.id is None: 
        temp_file = uuid.uuid4().hex
        return f"blog/posts/temp/{temp_file}{ext}"
    else:
        return f"blog/posts/featured_image/{instance.id}/featured_image{ext}"




class Category(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        )
    

    title_en = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
        )
    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs ):

        if not self.slug:
            
            if self.title_en:
                base_slug = slugify(self.title_en)
            else:
                base_slug = slugify(self.title)

            if not base_slug:
                base_slug = "category"

            slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)







# class Post(models.Model):

#     class Status(models.TextChoices):
#         DRAFT = "draft", "Draft"
#         PUBLISHED = "published", "Published"
#         ARCHIVED = "archived","Archived"



#     featured_image = models.ImageField(
#         upload_to=post_featured_image_avatar_path,
#         blank=True,
#         verbose_name='Featured Image',
#         validators=[validate_image_dimensions]
#     )

#     title_en = models.CharField(max_length=255,
#                             unique=True,
#                             db_index=True,
#                             blank=True,
#                             null=True)
    
#     title = models.CharField(max_length=255,
#                              unique=True,
#                              db_index=True,
#                              blank=False)
    
#     excerpt = models.TextField(
#         blank=True,
#         help_text="Short summary of the post"
#     )
    
#     content = models.TextField()
    
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='posts'
        
#     )



#     # category = models.ForeignKey(
#     #     Category,
#     #     on_delete=models.SET_DEFAULT,
#     #     related_name="posts",
#     #     )
    
    
#     # tags = 'x'
    
    
    
#     status = models.CharField(max_length=20, choices=Status, default=Status.DRAFT)
    
#     # views_count = 'x'
    
#     # reading_time = 'x'
    
#     # slug = 'x'
    
#     # login_required = 'x'
    
#     # created_date = 'x'
    
#     # updated_date = 'x'
    
    
#     # published_date = 'x'
    
#     # meta_description = 'x'
    
#     # meta_keywords = 'x'



#     def save(self, *args, **kwargs):
#         if not self.excerpt:
#             clean_content = strip_tags(self.content)
#             self.excerpt = Truncator(clean_content).words(30)


#         is_new = self.pk is None
#         old_image_path = None
        
#         if not is_new:
#             try:
#                 old_image_path = Post.objects.get(pk=self.pk).featured_image.path
#             except (ObjectDoesNotExist, ValueError):
#                 old_image_path = None
#         super().save(*args, **kwargs)
            

#         if is_new and self.featured_image:
#             temp_path = self.featured_image.path
#             _, ext = os.path.splitext(temp_path)

#             final_dir = f"blog/posts/featured_image/{self.pk}"
#             final_path = f"{final_dir}/featured_image{ext}"

#             full_final_dir = os.path.join(settings.MEDIA_ROOT, final_dir)
#             os.makedirs(full_final_dir, exist_ok=True)


#             final_full_path = os.path.join(settings.MEDIA_ROOT, final_path)
#             shutil.move(temp_path, final_full_path)
        

#             self.featured_image.name = final_path
#             super().save(update_fields=["featured_image"])
            
#         if old_image_path and self.featured_image and old_image_path != self.featured_image.path:
#             if os.path.exists(old_image_path):
#                 os.remove(old_image_path)



#     def __str__(self) -> str:
        return self.title