from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from bookings.models import Booking, Deposit


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PaymentTransaction(TimeStampedModel):
    class Status(models.TextChoices):
        INITIATED = "initiated", _("Initiated")
        SUCCEEDED = "succeeded", _("Succeeded")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
    )
    deposit = models.ForeignKey(
        Deposit,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="LYD")
    method = models.CharField(max_length=30)
    provider = models.CharField(max_length=60, blank=True)
    reference = models.CharField(max_length=120, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIATED)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("-created_at",)


class Payout(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PROCESSING = "processing", _("Processing")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")

    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payouts",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="LYD")
    reference = models.CharField(max_length=120, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)
