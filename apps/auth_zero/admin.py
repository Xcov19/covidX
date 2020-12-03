from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.auth_zero import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    # TODO(codecakes): add later
    pass
