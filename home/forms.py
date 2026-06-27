

from django import forms
from home.models import ContactMessage
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


class ContactMessageForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject',
                  'message', 'subscribe_to_newsletter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = False
        self.fields['email'].required = False
