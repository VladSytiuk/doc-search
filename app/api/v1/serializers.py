from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Documents

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = User
        fields = ("password", "username", "email", "id")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "id")


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ("document",)
