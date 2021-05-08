from django.http.response import Http404
from rest_framework import viewsets, status
from .models import Product
from .serializers import *
from products.permisssions import IsProductOwner
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

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

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()

class ProductImagesList(APIView):
    def get(self, request, product_id):
        images = ProductImage.objects.filter(product__id = product_id)
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        owner = request.user
        product = Product.objects.filter(id = product_id).first()
        if product is None:
            raise Http404
        serializer = ProductImageSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_products(request):
    owner = request.user
    products = Product.objects.filter(owner = owner)
    serializer = ProductSerializer(products, many = True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)