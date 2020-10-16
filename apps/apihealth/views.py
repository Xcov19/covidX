from covidx.apps.apihealth.serializer import ApiHealthSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

# from django.contrib.auth.models import User


@permission_classes((permissions.AllowAny,))
class ApiHealthViewSet(viewsets.ViewSet):
    """API Health Check which will returns 200."""

    serializer = ApiHealthSerializer
    queryset = get_user_model().objects.none

    def retrieve(self, _request, *args, **kwargs):
        return Response(ApiHealthSerializer().data)
