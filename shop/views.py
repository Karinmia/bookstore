import logging

from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Book
from .forms import BookForm

db_logger = logging.getLogger('db')


def book_list(request):
    books = Book.objects.all()

    if "new-first" in request.GET:
        books = books.order_by('-publish_date')
    elif "old-first" in request.GET:
        books = books.order_by('publish_date')

    db_logger.info('Read all the books.')

    return render(request, 'shop/book_list.html', {'books': books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)

    db_logger.info('Get details for book with id: {}'.format(book.pk))

    return render(request, 'shop/book_details.html', {'book': book})


def book_edit(request, pk=None):
    book = get_object_or_404(Book, pk=pk) if pk else None

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()

            if pk:
                db_logger.info('Successfully edited book with id: {}'.format(book.pk))
            else:
                db_logger.info('Successfully created new book with id: {}'.format(book.pk))

            return redirect('book_details', pk=book.pk)
    else:
        form = BookForm(instance=book)

    if pk:
        action = reverse(book_edit, args=[pk])
    else:
        action = reverse(book_edit)

    return render(request, 'shop/book_edit.html', {'form': form, 'action': action})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        book_id_ = book.pk
        book.delete()
        db_logger.info('Deleted book with id: {}'.format(book_id_))
    except:
        db_logger.info('Can not delete this book.')
    return redirect('book_list')
