from django.urls import path
from .views import StudentCreateView, GuestCreateView, AdminCreateView, upload_file_to_drive, view_paper, download_paper

urlpatterns = [
    path('register/student/', StudentCreateView.as_view(), name='register-student'),
    path('register/guest/', GuestCreateView.as_view(), name='register-guest'),
    path('register/admin/', AdminCreateView.as_view(), name='register-admin'),
    path('upload-to-drive/', upload_file_to_drive, name='upload_to_drive'),
    path('view-paper/<str:file_id>/', view_paper, name='view_paper'),
    path('download-paper/<int:paper_id>/', download_paper, name='download_paper'),
]