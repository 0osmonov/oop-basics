from rest_framework import permissions

from common.validators import validate_product_creator_age


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


class IsAdultToCreateProduct(permissions.BasePermission):
    """Проверяет возраст пользователя при создании Product по birthdate из JWT."""

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        birthdate = None
        token = getattr(request, 'auth', None)
        if token is not None:
            try:
                birthdate = token['birthdate']
            except (KeyError, TypeError):
                birthdate = token.payload.get('birthdate') if hasattr(token, 'payload') else None

        # если в токене нет — берём из пользователя (fallback)
        if birthdate is None and hasattr(request.user, 'birthdate'):
            birthdate = request.user.birthdate

        validate_product_creator_age(birthdate)
        return True
