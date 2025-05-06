from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import CreateUserSerializer, UserSerializer, ResearchPaperSerializer, DatasetSerializer, RequestSerializer, AuthorSerializer, CategorySerializer, KeywordSerializer, PermissionChangeLogSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ResearchPaper, Dataset, Request, Author, Category, Keyword, User, PermissionChangeLog
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.views import LoginView

class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'guest'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsAdminOrFaculty(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'faculty']

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=serializer.validated_data['password'])

class StudentCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(role='student', password=serializer.validated_data['password'])

class GuestCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(role='guest', password=serializer.validated_data['password'])

class AdminCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(role='admin', password=serializer.validated_data['password'])

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ResearchPaperListView(generics.ListAPIView):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAdminOrFaculty()]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.all()  # Use .all() to avoid RuntimeError
        if not user.is_authenticated:
            print("Unauthenticated user. Returning empty queryset.")
            return queryset.none()
        print("User Role:", user.role)
        print("Queryset Before Filtering:", queryset)
        if user.role == 'admin':
            print("Returning all research papers for admin.")
            return queryset
        if user.role == 'student':
            print("Returning all research papers for student.")
            return queryset
        elif user.role == 'guest':
            filtered_queryset = queryset.filter(access_setting='open')
            print("Returning open research papers for guest:", filtered_queryset)
            return filtered_queryset
        print("Returning empty queryset for unauthenticated user.")
        return queryset.none()

class DatasetListView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAdminOrFaculty()]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.all()  # Use .all() to avoid RuntimeError
        if user.is_authenticated:
            if user.role == 'student':
                return queryset
            elif user.role == 'guest':
                return queryset.filter(access_setting='open')
        return queryset.none()

class RequestCreateView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class KeywordListView(generics.ListAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.AllowAny]

class PermissionChangeView(generics.UpdateAPIView):
    queryset = PermissionChangeLog.objects.all()
    serializer_class = PermissionChangeLogSerializer
    permission_classes = [IsAdminOrFaculty]

    def perform_update(self, serializer):
        serializer.save(admin=self.request.user)

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'
#     redirect_authenticated_user = True
