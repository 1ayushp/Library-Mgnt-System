from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *

User = get_user_model()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminLibrarianOrReadOnly]
    # api/users/me
    @action(detail=False, methods=["GET"], url_path='me')
    def me(self, request):
        user = request.user
        rented_books = user.rented_books.all()
        serializer = self.get_serializer(rented_books, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsLibrarianUpdate_SelfUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'librarian']:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    # api/users/me
    @action(detail=False, methods=["GET"], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    # api/users/me/update
    @action(detail=False, methods=["PATCH"], url_path='me/update')
    def update_me(self, request):
        user = request.user
        new_username = request.data.get("username")
        current_password = request.data.get("password")
        new_password = request.data.get("new_password")
        updated = False
        if request.data.get("role"):
            return Response({"error": "Role cannot be updated."})

        if request.data.get("rented_books"):
            return Response({"error": "Books cannot be updated."})
            
        if not current_password:
            return Response({"error": "Current password is required."})

        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect."})

        # Change username if given
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                return Response({"error": "Username already taken."})
            user.username = new_username
            updated = True

        # Change password if given
        if new_password:
            user.set_password(new_password)
            updated = True

        if updated:
            user.save()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
