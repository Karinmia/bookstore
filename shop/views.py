import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Book
from .serializers import *
from .forms import BookForm


class BookList(APIView):
    """
    Get list of all currencies
    """
    serializer_class = BookSerializer

    @swagger_auto_schema(
        operation_id='Get books',
        security=[],
        tags=['Book'],
    )
    def get(self, request):
        books = Book.objects.all().order_by('-publish_date')
        data = self.serializer_class(books, many=True).data
        return Response({'books': data}, status=status.HTTP_200_OK)


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')
