from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bookings.models import Booking

from .models import Message, Notification
from .permissions import IsMessageParticipant
from .serializers import MessageSerializer, NotificationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageParticipant]

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.select_related("booking", "sender", "recipient").order_by("created_at")
        if getattr(user, "is_staff", False):
            return queryset
        return queryset.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        booking: Booking = serializer.validated_data["booking"]
        recipient = serializer.validated_data["recipient"]
        user = self.request.user

        if booking.tenant_id != user.id and booking.investor_id != user.id and not getattr(user, "is_staff", False):
            raise PermissionDenied("You are not part of this booking.")

        if recipient.id == user.id:
            raise PermissionDenied("Cannot send messages to yourself.")

        serializer.save(sender=user, recipient=recipient)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        if message.recipient_id != request.user.id and not getattr(request.user, "is_staff", False):
            raise PermissionDenied("Only the recipient can mark the message as read.")
        if not message.is_read:
            message.is_read = True
            message.read_at = timezone.now()
            message.save(update_fields=["is_read", "read_at"])
        return Response({"detail": "Message marked as read."}, status=status.HTTP_200_OK)


class NotificationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.read_at = timezone.now()
        instance.save(update_fields=["is_read", "read_at"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
