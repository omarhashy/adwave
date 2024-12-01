from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-data", views.upload_products, name="upload_data"),
    path("upload-sales", views.upload_sales, name="upload_sales"),
    path("send-emails", views.send_emails, name="send_emails"),
]
