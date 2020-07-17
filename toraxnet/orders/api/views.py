from rest_framework import generics, decorators, permissions
from rest_framework.response import Response
from django.db import transaction

from ..models import Cart, Order, OrderItem, CartItem, Product, DeliveryAdress
from .serializers import CartSerializer, CartItemSerializer, OrderItemSerializer, OrderSerializer


class CartUserListView(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        try:
            cart = self.request.user.cart
        except:
            cart = Cart.objects.create(user=self.request.user)
        queryset = cart.items
        return queryset


@decorators.api_view(['POST'])
@transaction.atomic
def add_item_to_cart(request):
    product_uuid = request.data['product']
    product = Product.objects.get(uuid=product_uuid)
    quantity = request.data['quantity']
    try:
        cart = request.user.cart
    except:
        cart = Cart.objects.create(user=request.user)
    try:
        item = cart.items.get(product=product_uuid)
        item.quantity = item.quantity + int(quantity)
        item.save()
        return Response(CartItemSerializer(item, context={'request': request}).data)
    except Exception as e:
        print(e)
        item = CartItem.objects.create(
            product=product, quantity=quantity, cart=cart)
        return Response(CartItemSerializer(item, context={'request': request}).data)


class OrderSingleItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer

    @transaction.atomic
    def perform_create(self, seriializer):
        total = seriializer.validated_data['price'] * \
            seriializer.validated_data['quantity']
        order = Order.objects.create(user=self.request.user)
        seriializer.save(order=order, total=total)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def update_cart(request):
    cart = request.user.cart
    items = request.data['items']

    for item in items:
        it = cart.items.get(product=item['product'])
        it.quantity = item['quantity']
        it = it.save()
    return Response(CartItemSerializer(cart.items, many=True, context={'request': request}).data)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.request.user.orders
        return queryset


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
@transaction.atomic
def order_many_items(request):
    delivery_address = request.data['delivery_address']

    delivery_address = DeliveryAdress.objects.create(**delivery_address)
    phone_number = request.data['phone_number']
    order = Order.objects.create(user=request.user, payment_state='PENDING',
                                 payment_type=request.data['payment_type'], total=0,
                                 phone_number=phone_number, delivery_address=delivery_address)

    items = request.user.cart.items.all()
    total = 0
    for item in items:
        sub_total = item.quantity * item.product.price
        OrderItem.objects.create(
            order=order, total=total, quantity=item.quantity,
            price=item.product.price, product_name=item.product.name, product=item.product)
        total = total + sub_total
    order.total = total
    order.save()
    items.all().delete()
    return Response('Votre ordre a ete place')


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
@transaction.atomic
def order_single_item(request):
    print(request.data)
    delivery_address = request.data['delivery_address']
    delivery_address = DeliveryAdress.objects.create(**delivery_address)
    phone_number = request.data['phone_number']
    order = Order.objects.create(user=request.user, phone_number=phone_number, delivery_address=delivery_address,
                                 payment_state='PENDING',
                                 payment_type=request.data['payment_type'], total=0)

    product = Product.objects.get(uuid=request.data['product'])
    quantity = request.data['quantity']
    total = 0
    sub_total = int(quantity) * product.price
    OrderItem.objects.create(
        order=order, total=sub_total, quantity=int(quantity),
        price=product.price, product_name=product.name, product=product)
    total = sub_total
    order.total = total
    order.save()
    return Response('Votre ordre a ete place')


class OrderSellerListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order = Order.objects.get(uuid=self.kwargs['uuid'])
        return order.items