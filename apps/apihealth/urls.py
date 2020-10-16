from django.urls import path

import apps.apihealth.views as views

urlpatterns = [
    path("", view=views.ApiHealthViewSet.as_view({"get": "retrieve"}), name="index"),
]
