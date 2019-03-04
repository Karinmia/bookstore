# from rest_framework import generics

from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
# from .serializers import SongsSerializer


def book_list(request):
    books = Book.objects.order_by('publish_date')
    return render(request, 'shop/book_list.html', {'books': books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_details.html', {'book': book})
