# Django ORM
from django.db import models

# Django settings (for referencing AUTH_USER_MODEL, etc.)
from django.conf import settings

# Django utilities for text processing and time handling
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.utils import timezone

# Django validation and exception handling
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import FileExtensionValidator


# Third-party packages
from slugify import slugify                # Generate URL-friendly slugs
from taggit.managers import TaggableManager # Tagging system for posts

# Image processing
from PIL import Image


# Python standard library
import os       # File system operations
import uuid     # Generate unique identifiers
import shutil   # File moving and management

# CKEditor
from django_ckeditor_5.fields import CKEditor5Field





# Validate uploaded image dimensions
# Ensures the image is within the allowed size range
def validate_image_dimensions(image):
        # Minimum allowed dimensions
    min_width, min_height = 640, 360

        # Maximum allowed dimensions
    max_width, max_height = 1920, 1080

    # If no image is provided, skip validation
    if not image:
        return
    
    try:
        # Open the uploaded image using Pillow
        with Image.open(image) as img:
            width, height = img.size
    except Exception:
         # Raise validation error if the file is not a valid image
        raise ValidationError("Uploaded file is not a valid image.")

    # Check if the image is smaller than the minimum allowed size
    if width < min_width or height < min_height:
        raise ValidationError(
            f"Image is too small. Minimum size is {min_width}x{min_height} pixels."
        )

    # Check if the image exceeds the maximum allowed size
    if width > max_width or height > max_height:
        raise ValidationError(
            f"Image is too large. Maximum size is {max_width}x{max_height} pixels."
        )



# Generate upload path for post featured images
# Handles temporary storage before the post instance is saved
def post_featured_image_avatar_path(instance, filename):
    # Extract file extension
    _, ext = os.path.splitext(filename)

    # If the post is not saved yet (no ID), store in a temporary location
    if instance.id is None: 
        temp_file = uuid.uuid4().hex
        return f"blog/posts/temp/{temp_file}{ext}"
    else:
        # After saving, store image in a directory based on post ID
        return f"blog/posts/featured_image/{instance.id}/featured_image{ext}"

# Retrieve or create the default category
# Used when a post does not have an assigned category
def get_default_category():
    category, _ = Category.objects.get_or_create(
        slug="uncategorized",
        defaults={
            "title": "بدون دسته‌بندی",
            "title_en": "Uncategorized",
        }
    )
    return category.pk

# Category model for organizing blog posts
class Category(models.Model):

    # Category title (Persian)
    title = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        )
    
    # Optional English title for the category
    title_en = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
        )

    # URL-friendly slug used in routes    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    # Timestamp when category was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp updated automatically on each save
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the category (used in admin and shell)
    def __str__(self):
        return self.title


    # Override save method to automatically generate a unique slug
    def save(self, *args, **kwargs ):

        # Generate slug only if it is not provided
        if not self.slug:

            # Prefer English title for slug generation if available
            if self.title_en:
                base_slug = slugify(self.title_en)
            else:
                base_slug = slugify(self.title)

            # Fallback slug if slugify returns empty
            if not base_slug:
                base_slug = "category"

            slug = base_slug
            counter = 1

            # Ensure slug uniqueness by appending a counter if needed
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Assign the final unique slug
            self.slug = slug

        # Call the original save method
        super().save(*args, **kwargs)




class Post(models.Model):

    # Post visibility and workflow status
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived","Archived"

    # Featured image for the post
    # Validated for extension and dimensions, uploaded using a dynamic path
    featured_image = models.ImageField(
        upload_to=post_featured_image_avatar_path,
        blank=True,
        verbose_name='Featured Image',
        validators=[
            FileExtensionValidator(["jpg","jpeg","png","webp"]),
            validate_image_dimensions
        ]
    )

    # Optional English title (used for slug generation or multilingual SEO)
    title_en = models.CharField(max_length=255,
                            blank=True,
                            null=True)
    
    # Main title of the post (required)
    title = models.CharField(max_length=255,
                             blank=False)

    # Short summary for previews, cards, and SEO
    excerpt = models.TextField(
        blank=True,
        help_text="Short summary of the post"
    )

    # Main body content (HTML or Markdown)   
    content = CKEditor5Field('Text', config_name='default')

    # Author of the post (nullable to avoid deletion cascade)   
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
        
    )


    # Post category (nullable, default handled in model logic)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        blank=True

        )
    
    # Tagging support using Django-taggit    
    tags = TaggableManager(blank=True)
    
    
    # Publication status (draft / published / archived)    
    status = models.CharField(
        max_length=20,
         choices=Status.choices,
         default=Status.DRAFT
        )
    
    # views_count = 'x'
    
 
    
    # Slug used for the post URL (auto-generated if empty)    
    slug =  models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

     # If enabled, user must be authenticated to view the post   
    login_required = models.BooleanField(default=False)

    # Creation timestamp
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    # Last update timestamp
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    
    # Timestamp for when the post was published
    # Indexed for faster queries (e.g., ordering by published date)    
    published_at = models.DateTimeField(
    null=True,
    blank=True,
    db_index=True
            )

    # SEO meta description (shown in search engines) 
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (max 160 characters)"
    )



    def save(self, *args, **kwargs):

        # Clean HTML tags for generating excerpt and SEO meta description
        clean_content = strip_tags(self.content or "")

        # Auto-generate excerpt if not provided
        if not self.excerpt:    
            self.excerpt = Truncator(clean_content).words(30)

        # Auto-generate meta description (SEO) if empty
        if not self.meta_description:
            self.meta_description = Truncator(clean_content).chars(160)

        # Check if this is a new post (used for image handling logic)
        is_new = self.pk is None
        old_image_path = None

        # On update, try to detect previous featured image path        
        if not is_new:
            try:
                old_image_path = Post.objects.get(pk=self.pk).featured_image.path
            except (ObjectDoesNotExist, ValueError):
                old_image_path = None

        # Auto-generate slug if empty (unique, SEO-friendly, fallback safe)
        if not self.slug:

             # Prefer English title for slug generation if available            
            if self.title_en:
                base_slug = slugify(self.title_en)
            else:
                base_slug = slugify(self.title)

            # Fallback slug if slugify returns an empty string
            if not base_slug:
                base_slug = "post"

            slug = base_slug
            counter = 1

            # Ensure slug uniqueness and avoid conflicts
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Set publish timestamp only the first time post is published
        if self.status == self.Status.PUBLISHED:
            if not self.published_at:
                self.published_at = timezone.now()

        # Assign default category if none is provided
        if not self.category_id:
            try:
                self.category_id = get_default_category()
            except Exception:
                pass

        # Save the post (first database write)
        super().save(*args, **kwargs)
            
        # Handle featured image relocation AFTER the post gets an ID
        if is_new and self.featured_image:

            # Temporary upload path
            temp_path = self.featured_image.path
            _, ext = os.path.splitext(temp_path)

            # Final directory and file path (based on post ID)
            final_dir = f"blog/posts/featured_image/{self.pk}"
            final_path = f"{final_dir}/featured_image{ext}"
            
            # Create directory if it doesn't exist
            full_final_dir = os.path.join(settings.MEDIA_ROOT, final_dir)
            os.makedirs(full_final_dir, exist_ok=True)

            # Move image from temp to final location
            final_full_path = os.path.join(settings.MEDIA_ROOT, final_path)
            shutil.move(temp_path, final_full_path)
        
             # Update model field with new relative path        
            self.featured_image.name = final_path

            # Update only the image field to avoid second full save
            super().save(update_fields=["featured_image"])
            
        # Delete previous image if a new one was uploaded
        if old_image_path and self.featured_image and old_image_path != self.featured_image.path:
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

    def __str__(self) -> str:
    # Human-readable representation of the post
        return self.title
    


class Comment(models.Model):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f'{self.name}|{self.post} '