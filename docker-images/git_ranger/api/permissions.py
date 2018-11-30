from rest_framework.permissions import BasePermission
from .models import AccessTokenlist


class IsOwner(BasePermission):
    """Custom permission class to allow only accesstokenlist owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the accesstokenlist owner."""
        if isinstance(obj, AccessTokenlist):
            return obj.owner == request.user
        return obj.owner == request.user