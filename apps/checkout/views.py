from apps.checkout.models import CartItem, Order, OrderItem
from apps.checkout.serializers import CartSerializer, EditCartSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

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

    @action(detail=False, methods=['post'], permission_classes=(IsAuthenticated,))
    def clear(self, request):
        user = request.user
        CartItem.objects.filter(user=user).delete()
        return Response('success')

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    @action(detail=False, methods=['post'], permission_classes=(IsAuthenticated,))
    def create_order(self):
        return Response("success")

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(user=user)

