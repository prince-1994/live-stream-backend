from apps.checkout.models import CartItem
from django.shortcuts import render
from apps.checkout.serializers import EditCartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class EditCartViewSet(viewsets.ModelViewSet):
    serializer_class = EditCartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)