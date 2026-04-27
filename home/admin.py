from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display= ("name", "email", "subject", "created_at", "subscribe_to_newsletter")
    search_fields= ("name", "email", "subject", "message")
    list_filter = ("subscribe_to_newsletter", )
    empty_value_display = "-empty-"
    list_per_page = 25
    ordering = ("-created_at",)


class Meta:
    verbose_name = 'Contact Message',
    verbose_name_plural = 'Contact Messages'