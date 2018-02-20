from rest_framework.permissions import BasePermission

SAFE_METHODS = ['POST']


class IsAuthenticatedOrWriteOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                    request.user and
                    request.user.is_authenticated()):
            return True
        return False
