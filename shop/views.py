# from rest_framework import generics
# from .serializers import SongsSerializer
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
from .forms import BookForm


def book_list(request):
    books = Book.objects.order_by('publish_date')
    return render(request, 'shop/book_list.html', {'books': books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_details.html', {'book': book})


def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            # book.publish_date = date.today()
            book.save()
            return redirect('book_details', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'blog/book_edit.html', {'form': form})


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('book_details', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'blog/book_edit.html', {'form': form})
