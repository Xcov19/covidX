from rest_framework import serializers


class ApiHealthSerializer(serializers.Serializer):
    success = serializers.BooleanField(
        required=True,
        label="Success Response",
    )
    data = {"success": True}
