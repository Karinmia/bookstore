from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('isbn', 'title', 'author', 'description', 'price', 'publish_date')
