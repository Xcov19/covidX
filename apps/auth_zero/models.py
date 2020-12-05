from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # email = models.EmailField(blank=False, verbose_name="email", unique=True)
    # username = models.CharField(blank=False, unique=True, max_length=256)
    # is_active = models.BooleanField(blank=False, default=False)
    # is_staff = models.BooleanField(blank=False, default=False)
    # is_superuser = models.BooleanField(blank=False, default=False)
    #
    # USERNAME_FIELD = "username"
    # EMAIL_FIELD = "email"

    class Meta:
        app_label = "auth_zero"
