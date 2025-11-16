from rest_framework import permissions


class IsMessageParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.sender_id == request.user.id
            or obj.recipient_id == request.user.id
            or getattr(request.user, "is_staff", False)
        )

