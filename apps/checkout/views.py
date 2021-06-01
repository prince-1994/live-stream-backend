from os import stat
from stripe.api_resources.customer import Customer
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

stripe.api_key = STRIPE_SECRET_KEY

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
        user = self.create_stripe_customer_if_not_present(request.user)
        (order_details_dict, total) = self.get_all_order_details(items=items,user=user)
        result_orders = self.create_all_orders(user, order_details_dict)
        metadata = {}
        i = 0
        for channel_id, order_dict in result_orders.items():
            order = order_dict["order"]
            order_items = order_dict["order_items"]
            for item in order_items:
                metadata[f'channel_{channel_id}_order_{order.id}_items_{item.id}'] = item.total_amount
            i+=1

        if total <= 0:
            return Response({"error" : "total cart value can not be less than or equal to 0"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = stripe.PaymentIntent.create(
            amount=int(total*100),
            currency="inr",
            payment_method_types=["card"],
            customer=user.stripe_customer,
            metadata=metadata,
            description=f"ordered {len(items)} items",
            # idempotency_key=str(user.id)  # study idempotency to improve paymentintent creation
            # statement_descriptor = ""     # statement descriptor can be set for invoices
        )
        
        for channel_id, order_dict in result_orders.items():
            order = order_dict["order"]
            order.stripe_payment_intent = response.id
            order.save()

        # print(order_details_dict)
        return Response({"client_secret": response.client_secret})
        # return Response({"client_secret" : response.client_secret}, status=status.HTTP_201_CREATED)

    def create_all_orders(self, user, order_details_dict):
        result_orders = {}
        for channel_id in order_details_dict:
            order_details = order_details_dict[channel_id]
            order = Order.objects.create(
                total_amount = order_details["total_amount"],
                user = user,
            )
            order.save()
            result_orders[channel_id] = {'order' : order, 'order_items' : []}
            for item in order_details['items']:
                order_item = OrderItem.objects.create(
                    order=order,
                    **item
                )
                result_orders[channel_id]['order_items'].append(order_item)

        return result_orders


    def create_stripe_customer_if_not_present(self, user):
        address = Address.objects.filter(user=user).first()
        stripe_customer = user.stripe_customer
        if stripe_customer == None or stripe_customer == "":
            name = f"{user.first_name} {user.last_name}"
            description = f"{name} - {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            response = stripe.Customer.create(
                name=name,
                description = description,
                address={
                    'city' : address.city,
                    'country' : address.country,
                    'line1' : address.line1,
                    'line2': address.line2,
                    'postal_code' : address.postal_code,
                    'state' : address.state,
                },
                email = user.email,
                metadata = {
                    'user_id' : user.id
                }
            )
            user.stripe_customer = response.id
            user.save()
        else:
            Response("No stripe customer found", status=status.HTTP_400_BAD_REQUEST)
            
        return user


    def get_all_order_details(self, items, user):
        order_details_dict = {}
        total = 0
        for item in items:
            product = Product.objects.get(pk=item["product"])
            quantity = item["quantity"]
            address = Address.objects.get(pk=item["address"])
            if address.user != user :
                return Response({"error" : "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            channel = product.channel
            channel_id = channel.id
            # commission = Commission.objects.filter(channel=channel, category=product.category).first()
            commission = Commission.objects.filter(channel=channel).first()
            if not channel_id in order_details_dict:
                order_details_dict[channel_id] = {"items":[], "total_amount" : 0}
            subtotal = product.selling_price * quantity
            total += subtotal
            
            order_details_dict[channel_id]['items'].append({
                'product' : product, 
                'quantity' : quantity,
                'total_amount' : subtotal,
                'price' : product.price,
                'selling_price' : product.selling_price,
                'commission' : commission,
                'address' : address,
            })
            order_details_dict[channel_id]['total_amount'] += subtotal
        print(total)
        return (order_details_dict, total)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(order__user=user)

