from rest_framework import serializers

from accounts.serializers import UserSerializer
from listings.models import Hall, HallSlot, Property

from .models import Booking, BookingEvent, Deposit


class BookingEventSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)

    class Meta:
        model = BookingEvent
        fields = ("id", "status", "notes", "actor", "created_at")
        read_only_fields = ("id", "actor", "created_at")


class DepositSerializer(serializers.ModelSerializer):
    recorded_by = UserSerializer(read_only=True)

    class Meta:
        model = Deposit
        fields = ("id", "amount", "method", "status", "reference", "recorded_by", "recorded_at")
        read_only_fields = ("id", "recorded_by", "recorded_at", "status")


class BookingSerializer(serializers.ModelSerializer):
    tenant = UserSerializer(read_only=True)
    investor = UserSerializer(read_only=True)
    deposits = DepositSerializer(many=True, read_only=True)
    events = BookingEventSerializer(many=True, read_only=True)
    property = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        allow_null=True,
        required=False,
    )
    hall = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(),
        allow_null=True,
        required=False,
    )
    hall_slot = serializers.PrimaryKeyRelatedField(
        queryset=HallSlot.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "tenant",
            "investor",
            "property",
            "hall",
            "hall_slot",
            "start_date",
            "end_date",
            "time_slot",
            "total_amount",
            "deposit_amount",
            "deposit_method",
            "deposit_paid",
            "status",
            "voice_message",
            "check_in_at",
            "check_out_at",
            "notes",
            "deposits",
            "events",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "id",
            "tenant",
            "investor",
            "deposit_paid",
            "status",
            "check_in_at",
            "check_out_at",
            "deposits",
            "events",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        property_obj = attrs.get("property")
        hall_obj = attrs.get("hall")
        if not property_obj and not hall_obj:
            raise serializers.ValidationError("You must reference a property or hall.")
        if property_obj and hall_obj:
            raise serializers.ValidationError("Booking cannot be linked to both property and hall simultaneously.")
        return attrs


class BookingStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Booking.Status.choices)
    notes = serializers.CharField(required=False, allow_blank=True)


class RecordDepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    method = serializers.ChoiceField(choices=Booking.DepositMethod.choices)
    reference = serializers.CharField(required=False, allow_blank=True)

