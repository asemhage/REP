from django.contrib import admin

from .models import Amenity, Hall, HallMedia, HallSlot, Property, PropertyAvailability, PropertyMedia


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 0


class PropertyAvailabilityInline(admin.TabularInline):
    model = PropertyAvailability
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "city", "property_type", "status")
    list_filter = ("property_type", "status", "city")
    search_fields = ("title", "city", "owner__username")
    inlines = [PropertyMediaInline, PropertyAvailabilityInline]


class HallMediaInline(admin.TabularInline):
    model = HallMedia
    extra = 0


class HallSlotInline(admin.TabularInline):
    model = HallSlot
    extra = 0


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "city", "status", "capacity")
    list_filter = ("status", "city")
    search_fields = ("name", "city", "owner__username")
    inlines = [HallMediaInline, HallSlotInline]
