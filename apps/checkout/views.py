from apps.checkout.models import CartItem
from apps.checkout.serializers import CartSerializer, EditCartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response

class EditCartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
    
    def get_serializer_class(self):
        if (self.request.method == "GET"):
            return CartSerializer
        return EditCartSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = EditCartSerializer(data=self.request.data)
        serializer.is_valid()
        cart_item = CartItem.objects.create(user=user,**serializer.validated_data)
        cart_item.save()
        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)