from django.urls import path
from .views import BookListView, BookDetailView

# app_name = 'books'

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]
