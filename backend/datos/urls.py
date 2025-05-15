"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from api.views import UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    UserListView, ResearchPaperListView, DatasetListView, RequestCreateView,
    AuthorListView, CategoryListView, KeywordListView
)
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_view, name='home'),
    # path("api/user/create/", UserCreateView.as_view(), name="user-create"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/users/", UserListView.as_view(), name="user-list"),
    path("api/research-papers/", ResearchPaperListView.as_view(), name="research-paper-list"),
    path("api/datasets/", DatasetListView.as_view(), name="dataset-list"),
    path("api/requests/create/", RequestCreateView.as_view(), name="request-create"),
    path("api/authors/", AuthorListView.as_view(), name="author-list"),
    path("api/categories/", CategoryListView.as_view(), name="category-list"),
    path("api/keywords/", KeywordListView.as_view(), name="keyword-list"),
    path('api/', include('api.urls')),
    
]
