from apps.channels.models import Channel
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class OrderItemEditPermission(BasePermission):
    def has_permission(self, request, view):
        if (type(request.user) == AnonymousUser):
            return False
        else :
            channel_id = request.query_params.get('channel')
            channel = Channel.objects.filter(pk=channel_id).first()
            if channel == None: 
                return False
            return channel.owner == request.user

    def has_object_permission(self, request, view, obj):
        if (type(request.user) == AnonymousUser):
            return False
        else :
            return obj.product.channel.owner == request.user
