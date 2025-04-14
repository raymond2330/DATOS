from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import CreateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=serializer.validated_data['password'])
