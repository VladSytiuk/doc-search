from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from app.models import Documents

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CreateUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("password", "username", "email")


class DocumentType(DjangoObjectType):
    class Meta:
        model = Documents
        fields = ("id", "document")
