from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from listings.models import Hall, HallSlot, Property


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")
        CANCELLED = "cancelled", _("Cancelled")
        COMPLETED = "completed", _("Completed")

    class DepositMethod(models.TextChoices):
        CARD = "card", _("Card")
        CASH = "cash", _("Cash")
        NONE = "none", _("None")

    property = models.ForeignKey(
        Property,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    hall = models.ForeignKey(
        Hall,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    hall_slot = models.ForeignKey(
        HallSlot,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_bookings",
    )
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investor_bookings",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    time_slot = models.CharField(max_length=20, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_method = models.CharField(
        max_length=10,
        choices=DepositMethod.choices,
        default=DepositMethod.NONE,
    )
    deposit_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    voice_message = models.FileField(upload_to="booking-voice/", null=True, blank=True)
    check_in_at = models.DateTimeField(null=True, blank=True)
    check_out_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("status",)),
            models.Index(fields=("tenant",)),
            models.Index(fields=("investor",)),
        ]

    def __str__(self) -> str:
        label = self.property or self.hall
        return f"Booking #{self.id} - {label}"


class Deposit(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        RECEIVED = "received", _("Received")
        RELEASED = "released", _("Released")
        FORFEITED = "forfeited", _("Forfeited")

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=Booking.DepositMethod.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_deposits",
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ("-created_at",)


class BookingEvent(TimeStampedModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="events")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="booking_events",
    )
    status = models.CharField(max_length=20, choices=Booking.Status.choices)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("created_at",)
