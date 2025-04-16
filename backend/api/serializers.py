from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    User, ResearchPaper, Dataset, Request, Author, PaperAuthor, DatasetAuthor,
    Category, Keyword, PaperKeyword, DatasetKeyword, PermissionChangeLog
)

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    institution = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'institution']

    def create(self, validated_data):
        # Hash the password and create the user
        institution = validated_data.pop('institution', '')  # Extract institution if provided
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as the username
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Optionally handle institution (e.g., save it to a related model or log it)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'username', 'email', 'avatar', 'institution', 'bio', 'join_date', 'last_login']

class ResearchPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPaper
        fields = ['id', 'title', 'abstract', 'journal', 'publication_details', 'access_setting', 'file_url', 'preview_url', 'category', 'uploaded_by']

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'title', 'description', 'version', 'size', 'file_url', 'preview_url', 'access_setting', 'uploaded_by']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'user', 'paper', 'dataset', 'purpose', 'reason_for_access', 'request_date', 'status']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'affiliation']

class PaperAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAuthor
        fields = ['id', 'paper', 'author']

class DatasetAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetAuthor
        fields = ['id', 'dataset', 'author']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'term']

class PaperKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperKeyword
        fields = ['id', 'paper', 'keyword']

class DatasetKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetKeyword
        fields = ['id', 'dataset', 'keyword']

class PermissionChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionChangeLog
        fields = ['id', 'request', 'admin', 'action', 'timestamp']
