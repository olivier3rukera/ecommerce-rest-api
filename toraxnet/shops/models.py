import uuid
from django.db import models
from toraxnet.accounts.models import Account


class Shop(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=150)
    owner = models.OneToOneField(Account, models.CASCADE)
