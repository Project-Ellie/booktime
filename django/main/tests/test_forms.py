from django.test import TestCase
from django.core import mail

from main import forms
from main.forms import UserCreationForm
import logging


class TestContactForm(TestCase):
    def test_valid_contact_us_form_sends_email(self):
        form = forms.ContactForm({
            'name': "Luke Skywalker",
            'message': "May the FORCE be with you."
        })

        self.assertTrue(form.is_valid())

        with self.assertLogs(logging.getLogger('main.forms'), level="INFO") as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Site message')

        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_contact_us_form(self):
        form = forms.ContactForm({
            'message': "Leia is a helluva cutie, ain't she?",
        })

        self.assertFalse(form.is_valid())


class TestSignupForm(TestCase):
    def test_valid_signup_form_sends_email(self):
        form = UserCreationForm(
            {
                'email': 'wgi@smurve.io',
                'password1': 'asdf1234.*',
                'password2': 'asdf1234.*'
             }
        )
        self.assertTrue(form.is_valid())

        with self.assertLogs(logging.getLogger('main.forms'), level='INFO') as cm:
            form.send_mail()

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, "Welcome to BookTime")

        self.assertGreaterEqual(len(cm.output), 1)
