from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.auth_zero import models

admin.site.register(models.User, UserAdmin)
