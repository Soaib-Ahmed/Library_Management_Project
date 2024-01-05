from django.urls import path

from .views import DepositMoneyView,ReturnBookView
# app_name = 'transactions'

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit_money'),
    # path('borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('return_book/<int:book_id>/', ReturnBookView.as_view(), name='return_book'),
]