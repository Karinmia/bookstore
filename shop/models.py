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
    publish_date = models.DateField(default=date.today, blank=True, null=True)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "price": self.price,
            "publish_date": self.publish_date
        }
