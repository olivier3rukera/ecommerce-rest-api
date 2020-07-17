import uuid
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.constraints import UniqueConstraint
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinLengthValidator
from toraxnet.accounts.models import Account
from toraxnet.shops.models import Shop
from django.contrib.postgres.fields import JSONField


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, default="Description du produit")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='FC')
    cover = models.ImageField(upload_to='products-covers/')
    picture_1 = models.ImageField(
        upload_to="products-pictures", null=True, blank=True)
    picture_2 = models.ImageField(
        upload_to="products-pictures", null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    discount_available = models.BooleanField(default=False)
    category = TreeForeignKey(
        'Category', models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Category(MPTTModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']