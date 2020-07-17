from django.db import models
import uuid

from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser


from .utils import UsernameValidator
from .helpers import get_default_email
username_validator = UsernameValidator()


class Account(AbstractUser):

    """    Class to represent a user acount
     it overide username, first_name,last_name and email
    """
    # overiden attributes
    username = models.CharField(max_length=20, unique=True,
                                validators=[username_validator],
                                error_messages={
                                    'unique': 'Cet numero existe deja',
                                }
                                )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)


class Address(models.Model):
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    avenue = models.CharField(max_length=150)
    number = models.IntegerField()
    account = models.OneToOneField(Account, models.CASCADE, null=True)