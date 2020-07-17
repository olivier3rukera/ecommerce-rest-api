from rest_framework import generics, decorators, permissions
from rest_framework.response import Response
from django.db import transaction

from ..models import Product, Category
from toraxnet.shops.models import Shop
from .serializers import ProductSerializer, ProductReadSerializer, CategorySerializer


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        name = self.request.query_params.get('name', None)

        if category is not None:
            cat = Category.objects.get(
                name=category).get_descendants(include_self=True)
            queryset = Product.objects.filter(
                category__in=cat)
            return queryset
        if name is not None:
            return Product.objects.filter(name__icontains=name)
        else:
            return Product.objects.all()


class ProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductReadSerializer
    queryset = Product.objects.all()


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
