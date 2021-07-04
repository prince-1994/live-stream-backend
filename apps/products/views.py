
from core.permissions import ReadOnly
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

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()