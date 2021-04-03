from .models import UserProfile
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class UserProfilePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.user == request.user

    def has_permission(self, request, view):
        if request.method == 'POST':
            return not UserProfile.objects.filter(user = request.user).exists()
        else :
            return True

class ChannelPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.user == request.user

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return type(request.user) != AnonymousUser
        else :
            return True

class VideoPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.channel.user == request.user

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return type(request.user) != AnonymousUser
        else :
            return True