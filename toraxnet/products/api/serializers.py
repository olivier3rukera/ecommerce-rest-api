from rest_framework import serializers

from ..models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    posted_at = serializers.ReadOnlyField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        fields = ['uuid', 'name', 'description',
                  'price', 'cover', 'posted_at', 'currency', 'category', 'picture_1', 'picture_2']
        model = Product

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        data['cover'] = self.context.get(
            'request').build_absolute_uri(instance.cover.url)
        return data


class ProductReadSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    posted_at = serializers.ReadOnlyField()
    category_name = serializers.ReadOnlyField(source='category.name')
    category = serializers.ReadOnlyField(source='category.uuid')

    class Meta:
        fields = ['uuid', 'name', 'description',
                  'price', 'cover', 'posted_at', 'currency', 'category', 'category_name', 'picture_1', 'picture_2']
        model = Product

    def to_representation(self, instance):
        data = super(ProductReadSerializer, self).to_representation(instance)
        data['cover'] = self.context.get(
            'request').build_absolute_uri(instance.cover.url)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'uuid']
