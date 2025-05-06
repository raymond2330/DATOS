from django.urls import path
from .views import StudentCreateView, GuestCreateView, AdminCreateView

urlpatterns = [
    # ...existing URL patterns...
    path('register/student/', StudentCreateView.as_view(), name='register-student'),
    path('register/guest/', GuestCreateView.as_view(), name='register-guest'),
    path('register/admin/', AdminCreateView.as_view(), name='register-admin'),
    
]