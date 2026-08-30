from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Модератор не может создавать товары'

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_staff:
            return request.method != 'POST'
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated and user.is_staff:
            return request.method in permissions.SAFE_METHODS or request.method in (
                'PUT',
                'PATCH',
                'DELETE',
            )
        return True


class IsProductOwner(permissions.BasePermission):
    message = 'Вы можете изменять только свои товары'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated and user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if not user.is_authenticated:
            return False
        return obj.author == user
