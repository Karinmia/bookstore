from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

from shop.models import Book
from shop.signals import on_update_book, on_delete_book


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        # import shop.signals
        post_save.connect(on_update_book, sender=Book)
        post_delete.connect(on_delete_book, sender=Book)
