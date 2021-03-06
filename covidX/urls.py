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
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()

SCHEMA_META = dict(
    title="CovidX: OpenAPI Spec",
    description="OpenAPI Spec Schema",
    version="0.0.1",
)

# Secure Django's admin login screen
admin.autodiscover()
admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path("openapi-schema/", get_schema_view(**SCHEMA_META), name="openapi-schema"),
    re_path(r"^login-rest-router/?$", include(router.urls)),
    re_path(
        r"^rest-auth/?$", include("rest_framework.urls", namespace="rest_framework")
    ),
    re_path(r"^apihealth/?$", include("apps.apihealth.urls")),
    path("auth0/", include("apps.auth_zero.urls")),
    path("admin/", admin.site.urls),
    re_path(r"^api/graphql/?$", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
