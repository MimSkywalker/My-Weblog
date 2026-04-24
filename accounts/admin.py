# --------------------------------------------------
# Django Admin configuration for the custom User model
# Extends Django's built‑in BaseUserAdmin to customize:
# - Displayed fields
# - Editable fields
# - Search options
# - Filters
# - Avatar preview in list & detail views
# --------------------------------------------------


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.html import format_html



# --------------------------------------------------
# Register the custom User model inside Django Admin
# --------------------------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):

   
    # Adds a date-based navigation bar in the admin for quick filtering
    date_hierarchy = "created_at"

    # Default placeholder for empty/null values in the admin table
    empty_value_display = "-empty-"
    
    # Columns displayed in the users list page inside Django admin
    list_display = ("id", "avatar_tag", "username", "email", "is_staff", "is_active", "date_joined")
    
    # Fields that can be edited directly from the users list view
    list_editable = ("is_active", 'is_staff')
    
    # Fields that can be searched from the admin search bar
    search_fields = ("username","email", 'first_name', 'last_name', )
    
    # Number of users shown per page in the admin list
    list_per_page = 20
    
    # Fields displayed as read‑only inside the detail view
    # (cannot be edited by admin)
    readonly_fields = ("avatar_preview", "created_at")
    
    # Filter options available in the sidebar
    list_filter = ['is_superuser','is_active','is_staff']

    # --------------------------------------------------
    # Field grouping and layout inside the user edit page
    # --------------------------------------------------
    fieldsets = (
        (None, {
            "fields": ("username", "password"),
        }),
        ("Personal info", {
            "fields": ("first_name", "last_name", "email", "phone"),
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important dates", {
            "fields": ("last_login", "created_at"),
        }),
        ("Profile", {
            "fields": ("avatar_preview", "avatar"),
        }),
    )



    # --------------------------------------------------
    # Show the user's avatar as a small 40x40px circle
    # inside the users list page
    # --------------------------------------------------
    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width = "40" height = "40" style="border-radius:50%;">', obj.avatar.url)
        return "-"

    # Display name of the column inside admin panel
    avatar_tag.short_description = "Avatar"

    # --------------------------------------------------
    # Show a large preview of the avatar inside user detail page
    # This helps admin see the full image before editing
    # --------------------------------------------------
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<a href="{}" target="_blank">'
            '<img src="{}" width="300" height="300" style="border-radius:10px; object-fit:cover; border: 1px solid #ccc; transition:0.2s;" '
            'onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">',
            obj.avatar.url,obj.avatar.url
            )
        return "-"
    
    # Label shown in admin for preview field
    avatar_preview.short_description = "Avatar Preview"