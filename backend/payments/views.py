from django.db.models import Q
from rest_framework import permissions, viewsets

from .models import PaymentTransaction, Payout
from .serializers import PaymentTransactionSerializer, PayoutSerializer


class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = PaymentTransaction.objects.select_related("booking", "deposit").order_by("-created_at")
        if getattr(user, "is_staff", False):
            return queryset
        return queryset.filter(
            Q(booking__tenant=user) | Q(booking__investor=user) | Q(deposit__recorded_by=user)
        ).distinct()


class PayoutViewSet(viewsets.ModelViewSet):
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Payout.objects.select_related("investor").order_by("-created_at")
        if getattr(user, "is_staff", False):
            return queryset
        return queryset.filter(investor=user)

    def perform_create(self, serializer):
        if not getattr(self.request.user, "is_staff", False):
            raise permissions.PermissionDenied("Only administrators can create payouts.")
        serializer.save()
