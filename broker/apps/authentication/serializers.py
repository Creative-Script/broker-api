from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Register a new user"""
    password = serializers.CharField(
        min_length=6,
        max_length=128,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['fname','lname','email', 'username', 'password']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)
