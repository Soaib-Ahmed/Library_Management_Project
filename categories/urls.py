from django.urls import path
from .views import category_list, filter_by_category

# app_name = 'categories'

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/<slug:category_slug>/', filter_by_category, name='filter_by_category'),
]
