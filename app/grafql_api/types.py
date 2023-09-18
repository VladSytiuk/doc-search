import graphene

from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType

from app.models import Documents


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class CreateUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("password", "username", "email", "first_name", "last_name")


class DocumentType(DjangoObjectType):
    class Meta:
        model = Documents
        fields = ("id", "document", "title", "owner", "created_at")


class QuestionType(graphene.ObjectType):
    question = graphene.String()
    document_id = graphene.Int()
    answer = graphene.String()
