from django.shortcuts import render
from .models import Category
from books.models import Book

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def filter_by_category(request, category_slug):
    categories = Category.objects.all()

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(categories=category)
        context = {'category': category, 'books': books}
    else:
        context = {'categories': categories}

    return render(request, 'filter_by_category.html', context)
