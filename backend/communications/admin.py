from django.contrib import admin

from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "sender", "recipient", "message_type", "created_at", "is_read")
    list_filter = ("message_type", "is_read")
    search_fields = ("sender__username", "recipient__username", "booking__id")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("user__username", "title")
