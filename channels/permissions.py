from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class IsChannelOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.owner == request.user

# class VideoPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         elif (type(request.user) == AnonymousUser):
#             return False
#         else :
#             return obj.channel.user == request.user

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         elif request.method == 'POST':
#             return type(request.user) != AnonymousUser
#         else :
#             return True