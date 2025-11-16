from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", _("Platform Admin")
        INVESTOR = "investor", _("Investor")
        TENANT = "tenant", _("Tenant")

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TENANT,
    )
    phone_number = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=8, default="ar")
    currency = models.CharField(max_length=3, default="LYD")
    timezone = models.CharField(max_length=64, default="Africa/Tripoli")
    is_identity_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

    @property
    def is_investor(self) -> bool:
        return self.role == self.Roles.INVESTOR

    @property
    def is_tenant(self) -> bool:
        return self.role == self.Roles.TENANT

