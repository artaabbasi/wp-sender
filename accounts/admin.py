from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telegram_id',)}),
    )


admin.site.register(User, MyUserAdmin)