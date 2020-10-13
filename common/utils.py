import enum

from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


class EnumChoice(enum.Enum):
    """Generic Enum class to fill choices in model fields."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def choices(cls):
        return [(field.name, field.value) for field in cls]
