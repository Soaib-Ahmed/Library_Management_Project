from django.views.generic import TemplateView
from books.models import Book
from categories.models import Category

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['categories'] = Category.objects.all()

        selected_category_slug = self.request.GET.get('category_slug')
        if selected_category_slug:
            context['selected_category'] = Category.objects.get(slug=selected_category_slug)
            context['books'] = Book.objects.filter(categories=context['selected_category'])
        else:
            context['selected_category'] = None

        return context
