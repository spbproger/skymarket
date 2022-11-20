# TODO здесь производится настройка пермишенов для нашего проекта
# from django.contrib.auth.models import AnonymousUser
# from rest_framework import permissions
#
# from users.models import UserRoles
#
#
# class AdUpdateDeletePermission(permissions.IsAuthenticatedOrReadOnly):
#     message = 'Update and Delete ads only for authors and admins.'
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if isinstance(request.user, AnonymousUser):
#             return False
#         if request.user.role == UserRoles.ADMIN:
#             return True
#         if request.user == obj.author:
#             return True
#         return False

from rest_framework.permissions import BasePermission
from users.managers import UserRoles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRoles.ADMIN


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user and obj.author == request.user