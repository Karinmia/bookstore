import uuid

from django.utils import timezone
from django.db import models


class HttpLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=18)
    request_type = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CRUDLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=18)
    request_type = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
