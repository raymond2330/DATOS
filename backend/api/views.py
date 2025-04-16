from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import CreateUserSerializer, UserSerializer, ResearchPaperSerializer, DatasetSerializer, RequestSerializer, AuthorSerializer, CategorySerializer, KeywordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ResearchPaper, Dataset, Request, Author, Category, Keyword, User

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=serializer.validated_data['password'])

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ResearchPaperListView(generics.ListAPIView):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer
    permission_classes = [permissions.AllowAny]

class DatasetListView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.AllowAny]

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
