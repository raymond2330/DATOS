from django.contrib.auth.models import User
from rest_framework import serializers

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
