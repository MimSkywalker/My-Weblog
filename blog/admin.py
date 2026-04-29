
from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display= ("id", "title", "title_en", "slug", "created_at")
    search_fields= ("title", "title_en", "slug")
    list_filter = ()
    readonly_fields = ('slug',)
    empty_value_display = "-empty-"
    list_per_page = 20
    ordering = ("-created_at",)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    date_hierarchy = "created_at"
    empty_value_display = "-empty-"
    search_fields= ("title", "title_en", "slug", "content")
    list_filter = ("status", "category", "author")
    list_per_page = 20

    list_editable = ("status", "published_at")
    ordering = ("-published_at","status","category","title")
    list_display = ("id", "featured_image_view", "title", "author", "category","status", "colored_status","login_required", "created_at", "published_at")
    readonly_fields = ("featured_image_preview", "created_at", "updated_at", "slug")
    list_display_links = ("title",)

    fieldsets = (
    ("Media", {
        "fields": ("featured_image", "featured_image_preview"),
    }),
    ("Main Content", {
        "fields": ("title", "title_en", "slug", "content", "excerpt")
    }),
    ("Meta & SEO", {
        "fields": ("meta_description",),
    }),
    ("Publishing", {
        "fields": ("status", "published_at", "login_required", "category", "tags")
    }),
    ("System Info (read only)", {
        "classes": ("collapse",),
        "fields": ("created_at", "updated_at")
    }),
)


    def featured_image_view(self, obj):
        if obj.featured_image and hasattr(obj.featured_image, "url"):
            return format_html(
                        '<a href="{0}" target="_blank">'
            '<img src="{0}" width="45" height="45" style="border-radius:6px; object-fit:cover;" />'
            '</a>',
                obj.featured_image.url)
        return "-"
    featured_image_view.short_description = "Image"


    def featured_image_preview(self, obj):
        if obj.featured_image and hasattr(obj.featured_image, "url"):
            return format_html(
                        '<a href="{0}" target="_blank">'
            '<img src="{0}" width="500" height="auto" style="border-radius:6px; object-fit:cover;" />'
            '</a>',
                obj.featured_image.url)
        return "-"
    featured_image_preview.short_description = "Image"


    def colored_status(self, obj):
        colors = {
            "draft": "gray",
            "published": "green",
            "archived": "red"
        }
        return format_html(
            '<span style="padding:3px 8px; color:white; background:{}; border-radius:4px; font-size:12px;">{}</span>',
            colors.get(obj.status, "gray"),
            obj.get_status_display()
        )
    colored_status.short_description = "Status"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("author", "category").prefetch_related("tags")


    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "email", "message")
    list_per_page = 20
    date_hierarchy = "created_at"
    empty_value_display = "-empty-"



