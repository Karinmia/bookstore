import uuid
from datetime import date

from django.db import models


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=18)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # image = models.ImageField(upload_to = 'img/', default = 'img/default.jpg')
    publish_date = models.DateField(default=date.today, blank=True, null=True)

    def publish(self):
        self.publish_date = date.today()
        self.save()

    def __str__(self):
        return self.title
