from django.urls import path
from . import views


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<uuid:pk>/', views.book_details, name='book_details'),
    path('book/new', views.book_new, name='book_new'),
    path('book/<uuid:pk>/edit/', views.book_edit, name='book_edit'),
]