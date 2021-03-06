from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish_date', 'price']
    ordering = ['title']


admin.site.register(Book, BookAdmin)
admin.site.site_header = "Books Management"
admin.site.site_title = "Books Management"
