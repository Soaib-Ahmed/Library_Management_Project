# from django.db import models
# from django.contrib.auth.models import User
# from books.models import Book

# class Transaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
#     transaction_type = models.CharField(max_length=20)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     balance_after_transaction = models.DecimalField(max_digits=8, decimal_places=2)

#     def save(self, *args, **kwargs):
#         # Set initial balance if it's a new transaction
#         if not self.id:
#             if self.transaction_type == 'deposit':
#                 # For a deposit transaction, increase the balance
#                 if hasattr(self.user, 'userprofile'):
#                     self.balance_after_transaction = self.user.userprofile.balance + self.amount
#             elif self.transaction_type == 'borrow':
#                 # For a borrow transaction, decrease the balance based on the borrowing price of the book
#                 if self.book and hasattr(self.user, 'userprofile'):
#                     borrowing_price = self.book.borrowing_price
#                     self.balance_after_transaction = self.user.userprofile.balance - borrowing_price

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.username} - {self.transaction_type} - {self.amount}"

from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from authentication.models import UserProfile

# class Transaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
#     transaction_type = models.CharField(max_length=20)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     balance_after_transaction = models.DecimalField(max_digits=8, decimal_places=2)

#     def save(self, *args, **kwargs):
#         # Set initial balance if it's a new transaction
#         if not self.id:
#             if self.transaction_type == 'deposit':
#                 # For a deposit transaction, increase the balance if the user has a userprofile
#                 user_profile, created = UserProfile.objects.get_or_create(user=self.user)
#                 user_profile.balance += self.amount
#                 user_profile.save()
#                 self.balance_after_transaction = user_profile.balance
#             elif self.transaction_type == 'borrow':
#                 # For a borrow transaction, decrease the balance based on the borrowing price of the book
#                 if self.book:
#                     user_profile, created = UserProfile.objects.get_or_create(user=self.user)
#                     borrowing_price = self.book.borrowing_price
#                     user_profile.balance -= borrowing_price
#                     user_profile.save()
#                     self.balance_after_transaction = user_profile.balance

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.username} - {self.transaction_type} - {self.amount}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('borrow', 'Borrow'),
        ('return', 'Return'),  # Add 'return' as a new transaction type
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance_after_transaction = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        # Set initial balance if it's a new transaction
        if not self.id:
            if self.transaction_type == 'deposit':
                # For a deposit transaction, increase the balance if the user has a userprofile
                user_profile, created = UserProfile.objects.get_or_create(user=self.user)
                user_profile.balance += self.amount
                user_profile.save()
                self.balance_after_transaction = user_profile.balance
            elif self.transaction_type == 'borrow':
                # For a borrow transaction, decrease the balance based on the borrowing price of the book
                if self.book:
                    user_profile, created = UserProfile.objects.get_or_create(user=self.user)
                    borrowing_price = self.book.borrowing_price
                    user_profile.balance -= borrowing_price
                    user_profile.save()
                    self.balance_after_transaction = user_profile.balance
            elif self.transaction_type == 'return':
                # For a return transaction, increase the balance based on the borrowing price of the book
                if self.book:
                    user_profile, created = UserProfile.objects.get_or_create(user=self.user)
                    borrowing_price = self.book.borrowing_price
                    user_profile.balance += borrowing_price  # Increase the balance
                    user_profile.save()
                    self.balance_after_transaction = user_profile.balance

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
