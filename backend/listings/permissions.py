from rest_framework import permissions


class IsInvestorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                getattr(request.user, "is_staff", False)
                or getattr(request.user, "is_investor", False)
            )
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and getattr(request.user, "is_staff", False):
            return True
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)

