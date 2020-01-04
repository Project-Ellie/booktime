from django.core.mail import send_mail
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UsernameField)
import logging
from main import models


logger = logging.getLogger(__name__)


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ('email',)
        field_classes = {'email': UsernameField}

    def send_mail(self):
        email = self.cleaned_data['email']
        logger.info("Sending signup email for %s", email)
        message = 'Welcome {}'.format(email)
        send_mail("Welcome to BookTime", message, "site@smurve.io", [email], fail_silently=True)
