from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions
from .serializers import CreateUserSerializer, UserSerializer, ResearchPaperSerializer, DatasetSerializer, RequestSerializer, AuthorSerializer, CategorySerializer, KeywordSerializer, PermissionChangeLogSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ResearchPaper, Dataset, Request, Author, Category, Keyword, User, PermissionChangeLog
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .utils import upload_to_google_drive
import os
from django.http import HttpResponse
from .utils import download_from_google_drive
from fitz import open as fitz_open
from django.template.loader import render_to_string


# set permissions for different user roles
class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'guest'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin']

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
        return [IsAdmin()]

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
        return [IsAdmin()]

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
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        serializer.save(admin=self.request.user)

# Decorator to check if the user is an admin
def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@api_view(['POST'])
@permission_classes([IsAdmin])
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

# TODO: Optimize the view_paper function by applying django's cache framework (In-memory, database, or file-based)
@api_view(['GET'])
@permission_classes([IsStudent | IsAdmin | IsGuest])
def view_paper(request, file_id):
    print("view_paper: Start")
    try:
        # Fetch the research paper by file_id
        paper = get_object_or_404(ResearchPaper, file_id=file_id)
        print(f"view_paper: Found paper with file_id {file_id}")

        # Determine the user's role
        user_role = request.user.role
        print(f"view_paper: User role is {user_role}")

        if user_role == 'guest':
            print("view_paper: Guest user detected. Attempting to download file.")
            file_content = download_from_google_drive(file_id)
            if not file_content:
                print("view_paper: Failed to download file.")
                return JsonResponse({"error": "Failed to download file."}, status=500)

            # Save the file temporarily
            temp_pdf_path = os.path.join('temp', f"{paper.title}.pdf")
            os.makedirs('temp', exist_ok=True)
            with open(temp_pdf_path, 'wb') as temp_file:
                temp_file.write(file_content)

            try:
                print("view_paper: Converting PDF to images using PyMuPDF.")
                pdf_document = fitz_open(temp_pdf_path)
                image_urls = []

                for page_number in range(1, min(4, len(pdf_document) + 1)):
                    page = pdf_document[page_number - 1]
                    pix = page.get_pixmap()
                    image_path = os.path.join('temp', f"{paper.title}_page_{page_number}.png")
                    pix.save(image_path)
                    image_urls.append(image_path)

                pdf_document.close()

                print("view_paper: Rendering preview HTML.")
                html_content = render_to_string('preview.html', {'images': image_urls})
                return HttpResponse(html_content)
            finally:
                print("view_paper: Cleaning up temporary files.")
                os.remove(temp_pdf_path)
                for image_path in image_urls:
                    os.remove(image_path)

        elif user_role in ['student', 'admin']:
            print("view_paper: Redirecting student/admin to Google Drive view URL.")
            view_url = paper.get_google_drive_view_url()
            if not view_url:
                print("view_paper: Google Drive view URL is None.")
                return JsonResponse({"error": "Google Drive view URL not found."}, status=404)
            return redirect(view_url)
        else:
            print("view_paper: Unauthorized role.")
            return JsonResponse({"error": "Unauthorized role."}, status=403)

    except Exception as e:
        print(f"view_paper: An unexpected error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred.", "details": str(e)}, status=500)

def download_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    if not paper.file_id:
        return HttpResponse("File ID not found.", status=404)

    file_content = download_from_google_drive(paper.file_id)
    if not file_content:
        return HttpResponse("Failed to download file.", status=500)

    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{paper.title}.pdf"'
    return response

@api_view(['POST'])
@permission_classes([IsGuest])
def request_access(request):
    print("request_access: Start")
    try:
        user = request.user
        paper_id = request.data.get('paper_id')
        purpose = request.data.get('purpose')
        reason_for_access = request.data.get('reason_for_access')

        if not paper_id or not purpose or not reason_for_access:
            return JsonResponse({"error": "Missing required fields."}, status=400)

        paper = get_object_or_404(ResearchPaper, id=paper_id)

        # Check if a request already exists
        existing_request = Request.objects.filter(user=user, paper=paper, status='pending').first()
        if existing_request:
            return JsonResponse({"error": "You already have a pending request for this paper."}, status=400)

        # Create a new access request
        access_request = Request.objects.create(
            user=user,
            paper=paper,
            purpose=purpose,
            reason_for_access=reason_for_access,
            status='pending'
        )

        print("request_access: Access request created successfully.")
        return JsonResponse({"message": "Access request submitted successfully.", "request_id": access_request.id}, status=201)

    except Exception as e:
        print(f"request_access: An unexpected error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred.", "details": str(e)}, status=500)