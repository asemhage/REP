from django.contrib import admin

from .models import Booking, BookingEvent, Deposit


class BookingEventInline(admin.TabularInline):
    model = BookingEvent
    extra = 0


class DepositInline(admin.TabularInline):
    model = Deposit
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "tenant", "investor", "start_date", "end_date", "deposit_paid")
    list_filter = ("status", "deposit_method", "deposit_paid")
    search_fields = ("id", "tenant__username", "investor__username")
    inlines = [DepositInline, BookingEventInline]


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("booking", "amount", "method", "status", "recorded_at")
    list_filter = ("method", "status")
    search_fields = ("booking__id", "reference")


@admin.register(BookingEvent)
class BookingEventAdmin(admin.ModelAdmin):
    list_display = ("booking", "status", "actor", "created_at")
    list_filter = ("status",)
