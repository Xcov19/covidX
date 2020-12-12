from django.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.auth_zero import views

urlpatterns = format_suffix_patterns(
    [
        path("", views.index, name="az_index"),
        path("dashboard", views.dashboard, name="az_dashboard"),
        path("logout", views.logout, name="az_logout"),
        path("", include("django.contrib.auth.urls"), name="az_login"),
        path("", include("social_django.urls"), name="az_login"),
    ]
)
