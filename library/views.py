from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer
from django.contrib.auth.models import User
from django.utils import timezone

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Loan ViewSet
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        loan.returned_date = timezone.now() # Mark the book as returned
        loan.save()
        loan.book.number_of_copies += 1 # Increase available copies
        loan.book.save()
        return Response({'status': 'book returned'})