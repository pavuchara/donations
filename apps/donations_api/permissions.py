from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyProfileOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj or request.method in SAFE_METHODS


class OnlyAuthorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.author or request.method in SAFE_METHODS


class OnlyOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.user or request.method in SAFE_METHODS
