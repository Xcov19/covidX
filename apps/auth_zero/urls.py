from django.urls import include
from django.conf.urls import url
from django.urls import path

from apps.auth_zero import views

urlpatterns = [
    path("", views.index, name="az_index"),
    path("dashboard", views.dashboard, name="az_dashboard"),
    path("logout", views.logout, name="az_logout"),
    path("", include("django.contrib.auth.urls"), name="az_login"),
    path("", include("social_django.urls"), name="az_login"),
]
