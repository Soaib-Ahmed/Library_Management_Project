from django import forms
from .models import Book, Review
from transactions.models import Transaction

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']

class BorrowBookForm(forms.Form):
    def __init__(self, user, book, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.book = book

    def clean(self):
        # Check if the user has sufficient balance for borrowing
        if self.user.userprofile.balance < self.book.borrowing_price:
            raise forms.ValidationError('You do not have enough balance to borrow this book.')

    def save(self):
        # Create a borrow transaction
        borrow_transaction = Transaction.objects.create(
            user=self.user,
            book=self.book,
            transaction_type='borrow',
            amount=-self.book.borrowing_price,
            balance_after_transaction=self.user.userprofile.balance - self.book.borrowing_price
        )

        # Update user's balance
        self.user.userprofile.balance -= self.book.borrowing_price
        self.user.userprofile.save()

        return borrow_transaction