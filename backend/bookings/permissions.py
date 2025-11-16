from rest_framework import permissions


class IsTenantOrInvestorParticipant(permissions.BasePermission):
    """
    Allow tenants/investors involved in the booking or admins.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user.is_authenticated
                and (
                    getattr(request.user, "is_staff", False)
                    or obj.tenant_id == request.user.id
                    or obj.investor_id == request.user.id
                )
            )
        if getattr(request.user, "is_staff", False):
            return True
        return obj.tenant_id == request.user.id or obj.investor_id == request.user.id


class IsTenantUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "is_tenant", False)


class IsInvestorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "is_investor", False)

