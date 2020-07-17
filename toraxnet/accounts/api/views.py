from requests.exceptions import HTTPError

from django.conf import settings
from django.http import HttpResponse

from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework import decorators
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from social_django.utils import psa

from .serializers import AccountSerializer
from ..models import Account

class AdminToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'username': user.username,
                'token': token.key,
                'uuid' : user.uuid,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email
            })
        else:
            return Response(data='user not admin', status=400)



def get_account_info(account: Account) -> dict:
    try:
        data = {}
        data['username'] = account.username
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['email'] = account.email
        data['password']= account.password
        data['uuid']= account.uuid
        print(data)
        return data
    except:
        print('error occured')
        return {}


class CreateUserMixin(mixins.CreateModelMixin, mixins.ListModelMixin):
    """
     create a user instance and return tokens
    """
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        username = serializer.validated_data['username']
        account = Account.objects.get(username=username)
        data = get_account_info(account)
        token = Token.objects.create(user=account)
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)


class CreateUser(generics.GenericAPIView, CreateUserMixin):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self,serializer):
        print(serializer.validated_data)
        user = serializer.save()


class CustomToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = get_account_info(user)
        data['token'] = token.key
        return Response(data)