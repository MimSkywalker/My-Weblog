from django.contrib import admin
from .models import Category


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