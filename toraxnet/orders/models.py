import uuid
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.constraints import UniqueConstraint
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinLengthValidator
from toraxnet.accounts.models import Account
from toraxnet.products.models import Product


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(Account, models.CASCADE, related_name='orders')
    delivery_address = models.ForeignKey('DeliveryAdress', models.CASCADE, null=True)
    phone_number = models.BigIntegerField()
    date = models.DateTimeField(auto_now=True)
    payment_type = models.CharField(
        max_length=30, validators=[MinLengthValidator(2)])
    payment_state = models.CharField(
        max_length=30, validators=[MinLengthValidator(2)])
    total = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    product = models.ForeignKey(Product, models.PROTECT, related_name='orders')
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, models.CASCADE, related_name='items')


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(Account, models.CASCADE)


class CartItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    product = models.ForeignKey(Product, models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, models.CASCADE, related_name='items')

    class Meta:
        constraints = [UniqueConstraint(
            fields=['product', 'cart'], name='no_duplicate_item')]

class DeliveryAdress(models.Model):
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    avenue = models.CharField(max_length=150)
    number = models.IntegerField()