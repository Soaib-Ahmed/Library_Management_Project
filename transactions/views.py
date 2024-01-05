
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import DepositForm,ReturnForm
from books.models import Book
from .models import Transaction
from authentication.models import UserProfile
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class DepositMoneyView(FormView):
    template_name = 'transactions/deposit_money.html'
    form_class = DepositForm

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        user = self.request.user

        user_profile, created = UserProfile.objects.get_or_create(user=user)

        deposit_transaction = Transaction.objects.create(
            user=user,
            transaction_type='deposit',
            amount=amount,
            balance_after_transaction=user_profile.balance + amount
        )

        
        user_profile.balance += amount
        user_profile.save()

        self.send_deposit_confirmation_email(user, amount, deposit_transaction.balance_after_transaction)

        messages.success(self.request, f'Deposit of ${amount} was successful!')
        return redirect('profile') 

    def form_invalid(self, form):
        messages.error(self.request, 'Deposit failed. Please check the form and try again.')
        return super().form_invalid(form)

    def send_deposit_confirmation_email(self, user, amount, balance_after_transaction):
        subject = 'Deposit Confirmation'
        template = 'transactions/deposit_confirmation_email.html'
        message = render_to_string(template, {
            'user': user,
            'amount': amount,
            'balance_after_transaction': balance_after_transaction,
        })

        send_email = EmailMultiAlternatives(subject, strip_tags(message), to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
    
class ReturnBookView(FormView):
    def post(self, request, book_id):
        # Retrieve the book
        book = get_object_or_404(Book, pk=book_id)

        # Check if the user has borrowed the book
        if request.user.transactions.filter(book=book, transaction_type='borrow').exists():
            # Calculate the refund amount (you might want to use the actual borrowing price here)
            refund_amount = book.borrowing_price

            # Add a transaction for returning the book
            return_transaction = Transaction.objects.create(
                user=request.user,
                book=book,
                transaction_type='return',
                amount=refund_amount,
                balance_after_transaction=request.user.userprofile.balance + refund_amount
            )

            # Update user's balance
            request.user.userprofile.balance += refund_amount
            request.user.userprofile.save()

            messages.success(request, f'Book "{book.title}" returned successfully. Refund: ${refund_amount}')
        else:
            messages.error(request, f'You have not borrowed the book "{book.title}".')

        # Redirect to the user's profile page after returning the book
        return redirect('profile')