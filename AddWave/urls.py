from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("index.urls")),
    path("auth/", include("user_auth.urls")),
    path("admin/", admin.site.urls),
]
