from django.contrib import admin
from .models import Category, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    search_fields= ("title", "title_en", "slug")
    list_filter = ()
    list_per_page = 20
    ordering = ("-created_at",)

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


