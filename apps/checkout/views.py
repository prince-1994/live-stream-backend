from apps.profiles.models import Address
from apps.payout.models import Commission
from apps.products.models import Category, Product
from apps.checkout.models import CartItem, Order, OrderItem
from apps.checkout.serializers import CartSerializer, EditCartSerializer, OrderItemSerializer, OrderSerializer, CreateOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from tslclone.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
import stripe

class EditCartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
    
    def get_serializer_class(self):
        if (self.request.method == "GET"):
            return CartSerializer
        return EditCartSerializer

    def create(self, request):
        user = request.user
        serializer = EditCartSerializer(data=request.data)
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

    @action(detail=False, methods=['post'], permission_classes=(IsAuthenticated,), url_path='create-order')
    def create_order(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        items = serializer.validated_data
        user = request.user
        orders = {}
        total = 0
        for item in items:
            product = Product.objects.get(pk=item["product"])
            quantity = item["quantity"]
            address = Address.objects.get(pk=item["address"])
            if address.user != user :
                return Response({"error" : "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            channel = product.channel
            channel_id = channel.id
            commission = Commission.objects.filter(channel=channel, category=product.category).first()
            
            if not channel_id in orders:
                orders[channel_id] = {"items":[], "total_amount" : 0}
            subtotal = product.selling_price * quantity
            total += subtotal
            
            orders[channel_id]['items'].append({
                'product' : product, 
                'quantity' : quantity,
                'collected_amount' : subtotal,
                'price' : product.price,
                'selling_price' : product.selling_price,
                'commission' : commission.id,
                'address' : address.id,
            })
            
        stripe.api_key = STRIPE_SECRET_KEY
        # response = stripe.PaymentIntent.create(
        #     amount=2000,
        #     currency="usd",
        #     payment_method_types=["card"],
        # )
        print(orders)
        

        return Response("success")

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(order__user=user)

