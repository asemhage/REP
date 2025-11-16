from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_identity_verified", "is_active")
    list_filter = ("role", "is_identity_verified", "is_staff", "is_active")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "language",
                    "currency",
                    "timezone",
                    "is_identity_verified",
                )
            },
        ),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "language",
                    "currency",
                    "timezone",
                )
            },
        ),
    )
    search_fields = ("username", "email", "phone_number")
    ordering = ("id",)
