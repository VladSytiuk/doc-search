import graphene

from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType

from app.models import Documents, UserKeys

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


class KeyType(DjangoObjectType):
    class Meta:
        model = UserKeys
        fields = ("key", "user", "documents_limit")


class AnalyticsUsersActivityType(graphene.ObjectType):
    id = graphene.Int()
    documents_amount = graphene.Int()
    questions_amount = graphene.Int()
    username = graphene.String()
