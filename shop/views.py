from rest_framework import generics

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Book
# from .serializers import SongsSerializer

def book_list(request):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'shop/book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_detail.html', {'book': book})
