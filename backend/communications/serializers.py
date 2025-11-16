from rest_framework import serializers

from accounts.serializers import UserSerializer
from bookings.serializers import BookingSerializer

from .models import Message, Notification


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    booking = BookingSerializer(read_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(
        source="recipient",
        queryset=UserSerializer.Meta.model.objects.all(),
        write_only=True,
    )
    booking_id = serializers.PrimaryKeyRelatedField(
        source="booking",
        queryset=BookingSerializer.Meta.model.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "booking",
            "booking_id",
            "sender",
            "recipient",
            "recipient_id",
            "message_type",
            "body",
            "voice_file",
            "is_read",
            "read_at",
            "created_at",
        )
        read_only_fields = ("id", "sender", "recipient", "booking", "is_read", "read_at", "created_at")


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "user", "title", "body", "payload", "is_read", "read_at", "created_at")
        read_only_fields = ("id", "user", "payload", "is_read", "read_at", "created_at")

