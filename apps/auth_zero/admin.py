from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.auth_zero import models


# TODO(codecakes): add from guardian.admin import GuardedModelAdmin


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    # TODO(codecakes): add on proper user model design
    pass
