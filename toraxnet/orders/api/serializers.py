from rest_framework import serializers
from toraxnet.products.models import Product
from ..models import Cart, CartItem, Order, OrderItem,DeliveryAdress

class OrderItemSerializer(serializers.ModelSerializer):

    uuid = serializers.ReadOnlyField()
    product_name = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['uuid', 'product_name', 'product', 'quantity', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    product_name = serializers.ReadOnlyField(source='product.name')
    unit_price = serializers.ReadOnlyField(source='product.price')
    #cover = serializers.SerializerMethodField()

    class Meta:
        fields = ['product', 'product_name', 'quantity', 'unit_price']
        model = CartItem

    def to_representation(self, instance):
        data = super(CartItemSerializer, self).to_representation(instance)
        data['cover'] = self.context.get(
            'request').build_absolute_uri(instance.product.cover.url)
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        fields = ['items']
        model = Cart

class DeliveryAdressSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all())

    class Meta:
        model = DeliveryAdress
        fields = ['city', 'street', 'avenue', 'number', 'order']



class OrderSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()
    payment_state = serializers.ReadOnlyField()

    class Meta:
        fields = ['uuid', 'date', 'payment_state',
                  'payment_type', 'total', 'delivery_address', 'phone_number']
        model = Order