from rest_framework import serializers
from ..models import Account, Address


class AccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdressSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all())

    class Meta:
        model = Address
        fields = ['city', 'street', 'avenue', 'number', 'account']
