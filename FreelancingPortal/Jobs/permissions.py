from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsEnterpriseUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and hasattr(request.user, 'enterprise_profile')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.enterprise.user == request.user