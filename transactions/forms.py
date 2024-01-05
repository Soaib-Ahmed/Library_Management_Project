

from django import forms
from .models import Transaction
from books.models import Book

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['amount']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'transaction_type', 'amount']

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        book = cleaned_data.get('book')

        if transaction_type == 'return' and not book:
            raise forms.ValidationError('For a return transaction, you must select a book.')

        return cleaned_data

class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book']

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')

        if not book:
            raise forms.ValidationError('For a return transaction, you must select a book.')

        return cleaned_data