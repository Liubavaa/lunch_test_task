from rest_framework.permissions import BasePermission

class IsRestaurantManager(BasePermission):
    """
    Custom permission to allow only restaurant managers to create or update menu.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsEmployee(BasePermission):
    """
    Custom permission to allow only employees to vote or view results.
    """
    def has_permission(self, request, view):
        return request.user.role == 'employee'
