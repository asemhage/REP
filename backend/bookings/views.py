from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from listings.models import HallSlot

from .models import Booking, BookingEvent, Deposit
from .permissions import IsInvestorUser, IsTenantOrInvestorParticipant, IsTenantUser
from .serializers import (
    BookingSerializer,
    BookingStatusSerializer,
    DepositSerializer,
    RecordDepositSerializer,
)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantOrInvestorParticipant]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Booking.objects.select_related("tenant", "investor", "property", "hall", "hall_slot")
            .prefetch_related("deposits", "events")
            .order_by("-created_at")
        )
        if getattr(user, "is_staff", False):
            return queryset
        return queryset.filter(Q(tenant=user) | Q(investor=user))

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsTenantUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        tenant = self.request.user
        property_obj = serializer.validated_data.get("property")
        hall_obj = serializer.validated_data.get("hall")
        hall_slot = serializer.validated_data.get("hall_slot")

        if property_obj:
            investor = property_obj.owner
        elif hall_obj:
            investor = hall_obj.owner
        else:
            raise PermissionDenied("A booking must target a property or hall.")

        if hall_obj and hall_slot and hall_slot.hall_id != hall_obj.id:
            raise PermissionDenied("Selected slot does not belong to the chosen hall.")

        booking = serializer.save(
            tenant=tenant,
            investor=investor,
            status=Booking.Status.PENDING,
        )
        BookingEvent.objects.create(
            booking=booking,
            actor=tenant,
            status=Booking.Status.PENDING,
            notes="Booking created by tenant.",
        )

    def perform_update(self, serializer):
        booking = serializer.save()
        BookingEvent.objects.create(
            booking=booking,
            actor=self.request.user,
            status=booking.status,
            notes="Booking updated.",
        )

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsInvestorUser])
    def update_status(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_value = serializer.validated_data["status"]
        notes = serializer.validated_data.get("notes", "")

        if booking.investor_id != request.user.id and not getattr(request.user, "is_staff", False):
            raise PermissionDenied("Only the investor can update booking status.")

        booking.status = status_value
        booking.save(update_fields=["status", "updated_at"])
        BookingEvent.objects.create(
            booking=booking,
            actor=request.user,
            status=status_value,
            notes=notes or f"Status changed to {status_value}.",
        )
        return Response(BookingSerializer(booking, context={"request": request}).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsInvestorUser])
    def record_deposit(self, request, pk=None):
        booking = self.get_object()
        serializer = RecordDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        deposit = Deposit.objects.create(
            booking=booking,
            amount=data["amount"],
            method=data["method"],
            status=Deposit.Status.RECEIVED,
            recorded_by=request.user,
            reference=data.get("reference", ""),
        )
        booking.deposit_paid = True
        booking.deposit_method = data["method"]
        booking.deposit_amount = data["amount"]
        booking.save(update_fields=["deposit_paid", "deposit_method", "deposit_amount", "updated_at"])

        BookingEvent.objects.create(
            booking=booking,
            actor=request.user,
            status=booking.status,
            notes="Deposit recorded.",
        )
        return Response(DepositSerializer(deposit, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsInvestorUser])
    def confirm_check_in(self, request, pk=None):
        booking = self.get_object()
        timestamp = timezone.now()
        booking.check_in_at = timestamp
        booking.updated_at = timestamp
        booking.save(update_fields=["check_in_at", "updated_at"])
        BookingEvent.objects.create(
            booking=booking,
            actor=request.user,
            status=booking.status,
            notes="Check-in confirmed.",
        )
        return Response({"detail": "Check-in confirmed."})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsInvestorUser])
    def confirm_check_out(self, request, pk=None):
        booking = self.get_object()
        timestamp = timezone.now()
        booking.check_out_at = timestamp
        booking.status = Booking.Status.COMPLETED
        booking.updated_at = timestamp
        booking.save(update_fields=["check_out_at", "status", "updated_at"])
        BookingEvent.objects.create(
            booking=booking,
            actor=request.user,
            status=booking.status,
            notes="Check-out confirmed.",
        )
        return Response({"detail": "Check-out confirmed."})
