from rest_framework import viewsets, status, filters
from .models import Product
from .serializers import *
from .permisssions import IsProductOwner
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class EditProductViewSet(viewsets.ModelViewSet):
    serializer_class = EditProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsProductOwner)

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        return Product.objects.filter(channel__id = channel_id)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_products(request):
    owner = request.user
    products = Product.objects.filter(owner = owner)
    serializer = ProductSerializer(products, many = True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)