import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book

db_logger = logging.getLogger('db')


# @receiver(post_save, sender=Book)
def on_update_book(sender, instance, created):
    print(instance)
    if created:
        print("created")
        db_logger.info('Successfully created new book with id: {}'.format(instance.pk))
    else:
        print("updated")
        db_logger.info('Successfully edited book with id: {}'.format(instance.pk))


# @receiver(post_delete, sender=Book)
def on_delete_book(sender, instance):
    print(instance)
    db_logger.info('Deleted book with id: {}'.format(instance.pk))
    print("deleted")
