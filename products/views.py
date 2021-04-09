from rest_framework import viewsets
from .models import Product
from .serializers import *
from tslclone.permissions import IsAuthenticatedAndOwner


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_queryset(self):
        owner = self.request.query_params.get('user')
        if owner is not None:
            return Product.objects.filter(owner__id = owner)
        return Product.objects.all()