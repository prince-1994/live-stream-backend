from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class ProductEditPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.channel.owner == request.user