from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Book, Review
from .forms import ReviewForm,BorrowBookForm
from transactions.forms import TransactionForm  
from transactions.models import Transaction
from django.contrib import messages
from django.views.generic.edit import FormView



class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView, FormView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'
    form_class = BorrowBookForm 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user 
        kwargs['book'] = self.get_object() 
        return kwargs

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        
        borrow_form = BorrowBookForm(data=request.POST, user=request.user, book=book)
        if borrow_form.is_valid():
            user = request.user
            borrowing_price = book.borrowing_price

            
            if user.userprofile.balance < borrowing_price:
                messages.error(request, 'You do not have enough balance to borrow this book.')
                return HttpResponseRedirect(request.path)  

            borrow_transaction = Transaction.objects.create(
                user=user,
                book=book,
                transaction_type='borrow',
                amount=borrowing_price,
                balance_after_transaction=user.userprofile.balance - borrowing_price
            )

            user.userprofile.balance -= borrowing_price
            user.userprofile.save()

            messages.success(request, f'You have successfully borrowed the book "{book.title}".')
            return HttpResponseRedirect(request.path) 
        
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.book = book
            new_review.save()

        return HttpResponseRedirect(request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = ReviewForm()
        borrow_form = BorrowBookForm(user=self.request.user, book=book) 

        user_has_borrowed = (
            self.request.user.is_authenticated and
            Transaction.objects.filter(user=self.request.user, book=book, transaction_type='borrow').exists()
        )

        context['reviews'] = reviews
        context['review_form'] = review_form
        context['borrow_form'] = borrow_form
        context['user_has_borrowed'] = user_has_borrowed  
        return context
