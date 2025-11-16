from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Amenity(TimeStampedModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Property(TimeStampedModel):
    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", _("Apartment")
        VILLA = "villa", _("Villa")
        CHALET = "chalet", _("Chalet")
        FARM = "farm", _("Farm")
        LAND = "land", _("Land")

    class Status(models.TextChoices):
        AVAILABLE = "available", _("Available")
        MAINTENANCE = "maintenance", _("Maintenance")
        UNAVAILABLE = "unavailable", _("Unavailable")
        SOLD = "sold", _("Sold")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    property_type = models.CharField(max_length=30, choices=PropertyType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deposit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    amenities = models.ManyToManyField(Amenity, related_name="properties", blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("city", "property_type")),
            models.Index(fields=("status",)),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.city})"


class PropertyMedia(TimeStampedModel):
    class MediaType(models.TextChoices):
        IMAGE = "image", _("Image")
        VIDEO = "video", _("Video")

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="properties/")
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.IMAGE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ("-is_primary", "id")


class PropertyAvailability(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="availability_blocks")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _("Property availability block")
        verbose_name_plural = _("Property availability blocks")


class Hall(TimeStampedModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", _("Available")
        MAINTENANCE = "maintenance", _("Maintenance")
        UNAVAILABLE = "unavailable", _("Unavailable")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="halls",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    capacity = models.PositiveIntegerField(default=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    morning_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    evening_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    full_day_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    amenities = models.ManyToManyField(Amenity, related_name="halls", blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


class HallMedia(TimeStampedModel):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="halls/")
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ("-is_primary", "id")


class HallSlot(models.Model):
    class Slot(models.TextChoices):
        MORNING = "morning", _("Morning")
        EVENING = "evening", _("Evening")
        FULL_DAY = "full_day", _("Full Day")

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    slot = models.CharField(max_length=20, choices=Slot.choices)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("hall", "date", "slot")
        ordering = ("date", "slot")
