from rest_framework.permissions import BasePermission

class ChannelEditPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(obj.owner, request.user)
        return request.user.is_authenticated and obj.owner == request.user