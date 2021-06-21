from rest_framework.exceptions import PermissionDenied
from tslclone.permissions import ReadOnly
from rest_framework import request, viewsets, status
from .models import Product
from .serializers import *
from .permisssions import ProductEditPermission
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (ReadOnly|ProductEditPermission,)
    filterset_fields = ['channel', 'category']
    search_fields = ['name', 'description']
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        serializer.save(channel=channel)
        return super().perform_create(serializer)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()