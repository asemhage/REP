from rest_framework import serializers

from accounts.serializers import UserSerializer
from bookings.serializers import BookingSerializer, DepositSerializer

from .models import PaymentTransaction, Payout


class PaymentTransactionSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    deposit = DepositSerializer(read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = (
            "id",
            "booking",
            "deposit",
            "amount",
            "currency",
            "method",
            "provider",
            "reference",
            "status",
            "metadata",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "booking", "deposit", "status", "created_at", "updated_at")


class PayoutSerializer(serializers.ModelSerializer):
    investor = UserSerializer(read_only=True)

    class Meta:
        model = Payout
        fields = (
            "id",
            "investor",
            "amount",
            "currency",
            "reference",
            "status",
            "scheduled_for",
            "notes",
            "created_at",
        )
        read_only_fields = ("id", "investor", "status", "created_at")

