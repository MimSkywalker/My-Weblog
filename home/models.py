from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    subscribe_to_newsletter = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} – {self.subject}"