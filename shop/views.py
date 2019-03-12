import logging

from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
from .forms import BookForm

db_logger = logging.getLogger('db')
http_logger = logging.getLogger('http')


def book_list(request):
    books = Book.objects.all()

    if "new-first" in request.GET:
        books = books.order_by('-publish_date')
    elif "old-first" in request.GET:
        books = books.order_by('publish_date')

    db_logger.debug('Read all the books.')
    http_logger.debug('{} {}'.format(request.method, request.path))

    return render(request, 'shop/book_list.html', {'books': books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)

    db_logger.debug('Get book details for id: {}'.format(book.pk))
    http_logger.debug('{} {}'.format(request.method, request.path))
    return render(request, 'shop/book_details.html', {'book': book})


def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            # book.publish_date = date.today()
            book.save()
            db_logger.debug('Successfully created book: {}'.format(book.pk))
            http_logger.debug('{} {}'.format(request.method, request.path))
            return redirect('book_details', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'shop/book_edit.html', {'form': form})


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            db_logger.debug('Successfully edited book: {}'.format(book.pk))
            http_logger.debug('{} {}'.format(request.method, request.path))
            return redirect('book_details', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'shop/book_edit.html', {'form': form})
