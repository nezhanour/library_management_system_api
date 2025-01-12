from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, User, Loan
from .serializers import BookSerializer, UserSerializer, LoanSerializer
from rest_framework.permissions import IsAuthenticated

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'], url_path='available')
    def available_books(self, request):
        available_books = Book.objects.filter(copies_available__gt=0)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Loan ViewSet
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['post'], url_path='check-out')
    def check_out_book(self, request, pk=None):
        user = request.user
        book = self.get_object()
        if book.copies_available > 0:
            Transaction.objects.create(user=user, book=book)
            book.copies_available -= 1
            book.save()
            return Response({'message': 'Book checked out successfully.'})
        return Response({'message': 'No copies available.'}, status=400)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        transaction = self.get_object()
        if not transaction.is_returned:
            transaction.is_returned = True
            transaction.return_date = timezone.now()
            transaction.save()
            transaction.book.copies_available += 1
            transaction.book.save()
            return Response({'message': 'Book returned successfully.'})
        return Response({'message': 'Book already returned.'}, status=400)
