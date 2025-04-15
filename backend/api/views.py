from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .serializers import CreateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ResearchPaper, Dataset, Request, Author, Category, Keyword
from .serializers import (
    ResearchPaperSerializer, DatasetSerializer, RequestSerializer,
    AuthorSerializer, CategorySerializer, KeywordSerializer
)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(
            password=serializer.validated_data['password'],
            role=serializer.validated_data.get('role', 'guest'),
            avatar=serializer.validated_data.get('avatar', ''),
            institution=serializer.validated_data.get('institution', ''),
            bio=serializer.validated_data.get('bio', '')
        )

class ResearchPaperListView(generics.ListCreateAPIView):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer

class DatasetListView(generics.ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class RequestListView(generics.ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class KeywordListView(generics.ListCreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class ResearchPaperViewSet(viewsets.ModelViewSet):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

