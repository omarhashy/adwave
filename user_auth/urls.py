# Import necessary modules
from django.contrib import admin  # Django admin module
from django.urls import path  # URL routing
from user_auth.views import *  # Import views from the authentication app
from django.conf import settings  # Application settings
from django.contrib.staticfiles.urls import (
    staticfiles_urlpatterns,
)  # Static files serving

# Define URL patterns
urlpatterns = [
    path("login/", login_page, name="login"),  # Login page
    path("logout/", user_logout, name="logout"),  # Login page
    path("register/", register_page, name="register"),  # Registration page
]
