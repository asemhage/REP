from django.contrib import admin

from .models import PaymentTransaction, Payout


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "amount", "currency", "status", "provider", "created_at")
    list_filter = ("status", "provider", "currency")
    search_fields = ("reference",)


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ("reference", "investor", "amount", "currency", "status", "scheduled_for")
    list_filter = ("status", "currency")
    search_fields = ("reference", "investor__username")
