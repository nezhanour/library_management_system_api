from django.db import models
from django.contrib.auth.models import User

# Book model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)  # Ensure unique ISBNs
    published_date = models.DateField()
    number_of_copies = models.IntegerField()

    def __str__(self):
        return f'{self.title} by {self.author}'


# Loan model
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Link to Book
    checked_out_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)  # Allow null for unreturned books

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'