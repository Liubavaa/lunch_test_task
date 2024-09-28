from rest_framework.permissions import BasePermission


class IsRestaurantAdmin(BasePermission):
    """Custom permission to allow only restaurant managers to create restaurants and upload menu for them."""
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsEmployee(BasePermission):
    """Custom permission to allow only employees to vote."""
    def has_permission(self, request, view):
        return request.user.role == 'employee'
