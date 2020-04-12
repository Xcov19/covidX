from django.urls import path

from . import views

urlpatterns = [path("", view=views.api_health, name="index")]
