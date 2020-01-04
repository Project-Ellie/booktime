from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib import auth

from main import forms, models


class TestHomePage(TestCase):
    def test_homepage_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookTime')

    def test_about_us_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about-us.html')
        self.assertContains(response, 'BookTime')

    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(
            response.context['form'], forms.ContactForm
        )


class TestSignupPage(TestCase):
    def test_sign_up_page_loads_correctly(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(response.context['form'], forms.UserCreationForm)

    def test_user_signup_page_submission_works(self):
        post_data = {
            'email': "user@domain.com",
            'password1': "abcabcabc",
            'password2': 'abcabcabc'
        }
        with patch.object(forms.UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(reverse('signup'), post_data)

        self.assertEquals(response.status_code, 302)
        self.assertTrue(models.User.objects.filter(email="user@domain.com").exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        mock_send.assert_called_once()


class TestAddressViews(TestCase):
    def test_address_list_page_returns_only_owned(self):
        user1 = models.User.objects.create_user("u1@bla.com", "supersecure")
        user2 = models.User.objects.create_user("u2@bla.com", "supersecure")
        models.Address.objects.create(
            user=user1,
            name="Kim Clarke",
            address1="flat1",
            address2="some av. 55b",
            city="Packinpah OH",
            country="us"
        )

        models.Address.objects.create(
            user=user2,
            name="Karen Clarke",
            address1="Huggeliweg 2",
            address2="Apt 2",
            city="Zurich ZH",
            country="ch"
        )

        self.client.force_login(user2)
        response = self.client.get(reverse('address_list'))
        self.assertEquals(response.status_code, 200)
        expected_list = models.Address.objects.filter(user=user2)
        self.assertEquals(list(response.context['object_list']),
                          list(expected_list))

    def test_address_create_stores_user(self):
        user1 = models.User.objects.create_user("u1@bla.com", "supersecure")
        post_data = {
            'name': "Kim Clarke",
            'address1': "flat1",
            'address2': "some av. 55b",
            'zip_code': 'MA12GS',
            'city': "Packinpah OH",
            'country': "us"
        }
        self.client.force_login(user1)
        self.client.post(reverse('address_create'), post_data)
        self.assertTrue(models.Address.objects.filter(user=user1).exists())
