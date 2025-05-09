from django.urls import path
from .views import StudentCreateView, GuestCreateView, AdminCreateView, upload_file_to_drive

urlpatterns = [
    # ...existing URL patterns...
    path('register/student/', StudentCreateView.as_view(), name='register-student'),
    path('register/guest/', GuestCreateView.as_view(), name='register-guest'),
    path('register/admin/', AdminCreateView.as_view(), name='register-admin'),
    path('upload-to-drive/', upload_file_to_drive, name='upload_to_drive'),
]