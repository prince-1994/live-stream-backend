from os import stat
from botocore import serialize
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

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsProductOwner,)
    filterset_fields = ['channel']
    search_fields = ['name', 'description']

    def get_queryset(self):
        is_channel_view = self.request.query_params.get('view') == 'channel'
        if is_channel_view and self.request.user.is_authenticated:
            channel = Channel.objects.filter(owner=self.request.user).first()
            if not channel:
                return Product.objects.none()
            return Product.objects.filter(channel=channel)
        return Product.objects.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            return Response({"error" : "channel does not exist"}, status= status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = Product.objects.create(channel=channel,**serializer.validated_data)
        obj.save()
        serializer = ProductSerializer(obj)
        return Response(serializer.data)

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