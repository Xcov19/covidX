"""Auth0 based models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserTypes(models.TextChoices):
    """Enum of User Types."""

    ADMIN = ("ADMIN", "admin")
    STAFF = ("STAFF", "staff")
    SUPPORT = ("SUPPORT", "support")
    PATIENT = ("PATIENT", "patient")


class User(AbstractUser):
    """Custom Auth User model."""

    default_user_type = UserTypes.PATIENT

    class Meta:
        app_label = "auth_zero"

    user_type = models.CharField(blank=False, max_length=20, default=default_user_type)

    def save(self, *args, **kwargs):
        """Set user type then save."""
        if not self.id:
            self.user_type = self.default_user_type
        if self.is_staff:
            self.user_type = UserTypes.STAFF
        if self.is_superuser:
            self.user_type = UserTypes.ADMIN
        return super().save(*args, **kwargs)


class UserTypeManager(models.Manager):
    """Common custom object manager for proxy user models."""

    def get_queryset(self):
        return User.objects.filter(user_type=self.model.default_user_type)


class PatientUser(User):
    objects = UserTypeManager()

    class Meta:
        proxy = True


class SupportUser(User):
    default_user_type = UserTypes.SUPPORT
    objects = UserTypeManager()

    class Meta:
        proxy = True


class StaffUser(User):
    default_user_type = UserTypes.STAFF
    objects = UserTypeManager()

    class Meta:
        proxy = True


class AdminUser(User):
    default_user_type = UserTypes.ADMIN
    objects = UserTypeManager()

    class Meta:
        proxy = True
