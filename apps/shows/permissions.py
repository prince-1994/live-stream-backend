from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from apps.channels.models import Channel

class IsShowOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.channel.owner == request.user

class IsVideoOwner(BasePermission):
    def has_permission(self, request, view):
        if (type(request.user) == AnonymousUser):
            return False
        else :
            channel_id = request.parser_context.get('kwargs').get('channel_id')
            channel = Channel.objects.filter(pk=channel_id).first()
            if channel == None: 
                return False
            return channel.owner == request.user

    def has_object_permission(self, request, view, obj):
        if (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.channel.owner == request.user