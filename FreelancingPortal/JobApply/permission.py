from rest_framework.permissions import BasePermission

class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'freelancer') and request.user.freelancer is not None:
            return True