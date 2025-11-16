from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Amenity, Hall, HallSlot, Property, PropertyAvailability
from .permissions import IsInvestorOrAdmin, IsOwnerOrAdmin
from .serializers import (
    AmenitySerializer,
    HallSerializer,
    HallSlotSerializer,
    PropertyAvailabilitySerializer,
    PropertySerializer,
)


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = (
            Property.objects.select_related("owner")
            .prefetch_related("amenities", "media", "availability_blocks")
            .order_by("-created_at")
        )
        city = self.request.query_params.get("city")
        status_param = self.request.query_params.get("status", Property.Status.AVAILABLE)
        property_type = self.request.query_params.get("property_type")

        if city:
            queryset = queryset.filter(city__iexact=city)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        return queryset

    def get_permissions(self):
        if self.action in ("list", "retrieve", "availability"):
            return [permissions.AllowAny()]
        if self.action in ("destroy", "update", "partial_update"):
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated(), IsInvestorOrAdmin()]

    def perform_create(self, serializer):
        user = self.request.user
        if not getattr(user, "is_investor", False) and not user.is_staff:
            raise PermissionDenied("Only investors can create properties.")
        serializer.save(owner=user)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def availability(self, request, pk=None):
        property_obj = self.get_object()
        serializer = PropertyAvailabilitySerializer(property_obj.availability_blocks.all(), many=True)
        return Response(serializer.data)


class PropertyAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        queryset = PropertyAvailability.objects.select_related("property", "property__owner")
        user = self.request.user
        if getattr(user, "is_staff", False):
            return queryset
        return queryset.filter(property__owner=user)

    def perform_create(self, serializer):
        property_obj = serializer.validated_data["property"]
        if property_obj.owner != self.request.user:
            raise PermissionDenied("Cannot edit availability for another owner's property.")
        serializer.save()


class HallViewSet(viewsets.ModelViewSet):
    serializer_class = HallSerializer

    def get_queryset(self):
        queryset = (
            Hall.objects.select_related("owner")
            .prefetch_related("amenities", "media", Prefetch("slots", queryset=HallSlot.objects.order_by("date")))
            .order_by("-created_at")
        )
        city = self.request.query_params.get("city")
        status_param = self.request.query_params.get("status", Hall.Status.AVAILABLE)
        if city:
            queryset = queryset.filter(city__iexact=city)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def get_permissions(self):
        if self.action in ("list", "retrieve", "slots"):
            return [permissions.AllowAny()]
        if self.action in ("destroy", "update", "partial_update"):
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated(), IsInvestorOrAdmin()]

    def perform_create(self, serializer):
        user = self.request.user
        if not getattr(user, "is_investor", False) and not user.is_staff:
            raise PermissionDenied("Only investors can create halls.")
        serializer.save(owner=user)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def slots(self, request, pk=None):
        hall = self.get_object()
        serializer = HallSlotSerializer(hall.slots.all(), many=True)
        return Response(serializer.data)


class HallSlotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HallSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        hall_id = self.kwargs.get("hall_pk")
        queryset = HallSlot.objects.all().order_by("date", "slot")
        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)
        return queryset
