from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'role', None) == 'ADMIN')

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'role', None) == 'RECRUITER')

class IsSeeker(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'role', None) == 'SEEKER')
