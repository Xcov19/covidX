from django.urls import path

import apps.apihealth.views as views

urlpatterns = [path("", view=views.api_health, name="index")]
