"""covidX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from common import utils

urlpatterns = [
    # See: https://www.django-rest-framework.org/#installation
    re_path(r"^login-rest-router/?$", include(utils.router.urls)),
    re_path(
        r"^rest-auth/?$", include("rest_framework.urls", namespace="rest_framework")
    ),
    re_path(r"^apihealth/?$", include("apps.apihealth.urls")),
    path("admin/", admin.site.urls),
    re_path("^auth0/?$", include("apps.auth_zero.urls")),
    re_path(r"^api/graphql/?$", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
