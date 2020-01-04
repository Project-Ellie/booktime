import logging
from django.contrib.auth import authenticate
from django import forms

logger = logging.getLogger(__name__)


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email/password combination.")
            logger.info("Authentication successful for email=%s", email)
        return self.cleaned_data

    def get_user(self):
        return self.user
