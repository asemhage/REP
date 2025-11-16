from rest_framework import serializers

from .models import (
    Amenity,
    Hall,
    HallMedia,
    HallSlot,
    Property,
    PropertyAvailability,
    PropertyMedia,
)


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("id", "name", "slug")


class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ("id", "file", "media_type", "is_primary")
        read_only_fields = ("id",)


class PropertyAvailabilitySerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = PropertyAvailability
        fields = ("id", "property", "start_date", "end_date", "reason")
        read_only_fields = ("id",)


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    media = PropertyMediaSerializer(many=True, read_only=True)
    amenities = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        required=False,
    )
    availability_blocks = PropertyAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "address",
            "city",
            "latitude",
            "longitude",
            "property_type",
            "status",
            "daily_rate",
            "monthly_rate",
            "sale_price",
            "deposit_percentage",
            "amenities",
            "media",
            "availability_blocks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "owner", "created_at", "updated_at", "status")


class HallMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallMedia
        fields = ("id", "file", "is_primary")
        read_only_fields = ("id",)


class HallSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallSlot
        fields = ("id", "date", "slot", "is_reserved")
        read_only_fields = ("id", "is_reserved")


class HallSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    amenities = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        required=False,
    )
    media = HallMediaSerializer(many=True, read_only=True)
    slots = HallSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Hall
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "address",
            "city",
            "capacity",
            "status",
            "morning_rate",
            "evening_rate",
            "full_day_rate",
            "deposit_percentage",
            "amenities",
            "media",
            "slots",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "owner", "status", "created_at", "updated_at")

