
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class CustomLoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(widget=forms.PasswordInput, label="کلمه عبور")
    captcha = ReCaptchaField(widget=ReCaptchaV3)
