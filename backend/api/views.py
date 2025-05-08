from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import CreateUserSerializer, UserSerializer, ResearchPaperSerializer, DatasetSerializer, RequestSerializer, AuthorSerializer, CategorySerializer, KeywordSerializer, PermissionChangeLogSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ResearchPaper, Dataset, Request, Author, Category, Keyword, User, PermissionChangeLog
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import upload_to_google_drive
import os

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

from .models import ResearchPaper, Dataset

@api_view(['POST'])
def upload_file_to_drive(request):
    file_type = request.data.get('file_type')  # Expecting 'dataset' or 'research_paper'
    title = request.data.get('title')
    description = request.data.get('description')
    category_id = request.data.get('category_id')

    if not file_type or file_type not in ['dataset', 'research_paper']:
        return JsonResponse({'error': 'Invalid or missing file_type. Must be "dataset" or "research_paper".'}, status=400)

    if not title:
        return JsonResponse({'error': 'Title is required.'}, status=400)

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    uploaded_file = request.FILES['file']
    file_path = os.path.join('temp', uploaded_file.name)

    # Save the file temporarily
    os.makedirs('temp', exist_ok=True)
    with open(file_path, 'wb') as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)

    try:
        # Define folder IDs for Research Papers and Datasets
        research_paper_folder_id = '1jrLtAfhsTnTo9ePASvUxj05BlWQplZBo'  # Replace with the actual folder ID
        dataset_folder_id = '1xlr1MfA4wsj8ReudK-s9-mm7S7e2EfD7'  # Replace with the actual folder ID

        # Determine the target folder based on file type
        if file_type == 'research_paper':
            folder_id = research_paper_folder_id
        elif file_type == 'dataset':
            folder_id = dataset_folder_id

        # Upload to the appropriate folder in Google Drive
        file_metadata = {
            'name': uploaded_file.name,
            'parents': [folder_id]
        }
        file_id = upload_to_google_drive(file_path, uploaded_file.name, file_metadata)

        # Get or create a default category if category_id is not provided
        if not category_id:
            category, _ = Category.objects.get_or_create(name='Default')
        else:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Invalid category_id provided.'}, status=400)

        # Save metadata to the database
        if file_type == 'dataset':
            Dataset.objects.create(title=title, description=description, file_id=file_id, uploaded_by=request.user)
        elif file_type == 'research_paper':
            ResearchPaper.objects.create(title=title, description=description, file_id=file_id, category=category, uploaded_by=request.user)

        return JsonResponse({'message': 'File uploaded successfully', 'file_id': file_id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        # Clean up the temporary file
        os.remove(file_path)

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'
#     redirect_authenticated_user = True
