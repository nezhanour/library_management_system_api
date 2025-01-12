from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, User, Loan
from .serializers import BookSerializer, UserSerializer, LoanSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import status

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='available')
    def available_books(self, request):
        available_books = Book.objects.filter(number_of_copies__gt=0)
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
        book = Book.objects.get(id=pk)  # Get the book by its ID (from URL)
        user = request.user  # Get the user from the request (authenticated user)

        # Check if the book has available copies
        if book.number_of_copies > 0:
            # Create a loan record for the user
            loan = Loan.objects.create(
                user=user,
                book=book,
                checked_out_date=timezone.now(),
                is_returned=False  # Ensure it's False when checked out
            )

            # Decrease the available copies of the book
            book.number_of_copies -= 1
            book.save()

            return Response({'message': 'Book checked out successfully.', 'loan_id': loan.id}, status=status.HTTP_200_OK)

        return Response({'message': 'No copies available for checkout.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        loan = self.get_object()

        # Check if the loan has already been returned
        if loan.is_returned:
            return Response({'message': 'Book already returned.'}, status=400)

        # Proceed with returning the book
        loan.is_returned = True
        loan.return_date = timezone.now()
        loan.save()

        # Increment the available copies of the book
        loan.book.number_of_copies += 1
        loan.book.save()

        return Response({'message': 'Book returned successfully.'})

