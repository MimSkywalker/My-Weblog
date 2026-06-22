

from django import forms
from home.models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject',
                  'message', 'subscribe_to_newsletter']
