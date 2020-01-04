from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from main import views, forms

urlpatterns = [

    path("login/",
         auth_views.LoginView.as_view(
             template_name="login.html",
             form_class=forms.AuthenticationForm
         ),
         name="login"),

    path("about-us/",
         TemplateView.as_view(template_name='about-us.html'),
         name="about_us"),

    path("",
         TemplateView.as_view(template_name='home.html'),
         name='home'),

    path("contact-us/",
         views.ContactUsView.as_view(),
         name='contact_us'),

    path("signup/",
         views.SignupView.as_view(),
         name="signup"),

    path("address/",
         views.AddressListView.as_view(),
         name="address_list"),

    path("address/create/",
         views.AddressCreateView.as_view(),
         name="address_create"),

    path("address/<int:pk>",
         views.AddressUpdateView.as_view(),
         name="address_update"),

    path("address/<int:pk>/delete",
         views.AddressDeleteView.as_view(),
         name="address_delete")
]
