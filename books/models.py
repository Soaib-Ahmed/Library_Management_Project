from django.db import models
from categories.models import Category
from authentication.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='books/media/uploads/', blank=True, null=True)
    borrowing_price = models.DecimalField(max_digits=8, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='books')
    user_reviews = models.ManyToManyField(User, through='books.Review')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book}"