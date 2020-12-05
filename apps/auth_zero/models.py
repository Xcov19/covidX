from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom Auth User model."""

    class Meta:
        app_label = "auth_zero"
