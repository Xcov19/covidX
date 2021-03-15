"""Auth0 based models."""
from typing import List
from typing import TypeVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction
from django.db.models import Q

from phonenumber_field.modelfields import PhoneNumberField

UserTypes_T = TypeVar("UserTypes_T", bound="UserTypes")
User_T = TypeVar("User_T", bound="User")
AccountTypes_T = TypeVar("AccountTypes_T", bound="AccountType")


class UserTypes(models.TextChoices):
    """Enum of User Types."""

    ADMIN = ("ADMIN", "admin")
    STAFF = ("STAFF", "staff")
    SUPPORT = ("SUPPORT", "support")
    PATIENT = ("PATIENT", "patient")


class User(AbstractUser):
    """Custom Auth User model."""

    default_user_type = UserTypes.PATIENT
    mobile = PhoneNumberField(blank=True)
    last_otp = models.CharField(blank=False, null=True, max_length=20)
    otp_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    class Meta:
        app_label = "auth_zero"

    @property
    def is_verified(self):
        return self.otp_verified and self.email_verified

    @property
    def user_types(self):
        return self.account_types  # pylint: disable=no-member

    def save(self, *args, **kwargs):
        """Set user type then save."""
        acc_levels: List[UserTypes_T] = []
        acc_type_ids: List[int]
        if self.username != "AnonymousUser":
            # Refer to auth0backend.Auth0.process_roles to see why
            if self.is_staff:
                acc_levels += [UserTypes.STAFF]
            if self.is_superuser:
                acc_levels += [UserTypes.ADMIN]
            if not self.id and not acc_levels:
                acc_levels += [self.default_user_type]
        super().save(*args, **kwargs)
        self.refresh_from_db()
        if acc_levels:
            self._update_acc_types(acc_levels)

    def _update_acc_types(self, acc_levels: List[UserTypes_T]):
        """New AccountType not currently associated."""
        new_acc_obj: List[AccountTypes_T] = []
        if not (
            existing_types_qs := AccountType.objects.filter(
                Q(user_type_level__in=acc_levels)
            )
        ):
            new_acc_obj += (
                AccountType(**dict(user_type_level=level)) for level in acc_levels
            )
        else:
            existing_levels = existing_types_qs.values_list(
                "user_type_level", flat=True
            )
            new_levels = set(acc_levels) - set(existing_levels)
            new_acc_obj += (
                AccountType(**dict(user_type_level=level)) for level in new_levels
            )
        update_existing_ids = existing_types_qs.values_list("id", flat=True)
        exclude_type_ids = AccountType.objects.values_list("id", flat=True)
        with transaction.atomic():
            # bulk create only non existent types
            AccountType.objects.bulk_create(new_acc_obj)
            # update with newly created account types
            update_existing_ids |= AccountType.objects.exclude(
                id__in=exclude_type_ids
            ).values_list("id", flat=True)
            settings.LOGGER.info(f"creating account roles: {update_existing_ids}")
            self.account_types.add(*update_existing_ids)  # pylint: disable=no-member


class AccountType(models.Model):
    """User can have many cccount types."""

    # TODO(codecakes): add more functionality
    user_type_level = models.CharField(
        blank=False,
        max_length=20,
        default=UserTypes.PATIENT,
        unique=True,
        choices=[(t, t.label) for t in UserTypes],
    )
    users = models.ManyToManyField(User, related_name="account_types")


class UserTypeManager(models.Manager):
    """Common custom object manager for proxy user models."""

    def get_queryset(self):
        return User.objects.filter(
            Q(account_types__user_type_level=self.model.default_user_type)
        )


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
