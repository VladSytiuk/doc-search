import graphene
from graphql_jwt.decorators import login_required
import graphql_jwt
from django.contrib.auth import get_user_model

from app.grafql_api.mutations.document import UploadDocumentMutation, DeleteDocumentMutation
from app.grafql_api.mutations.users import (
    UpdateUserMutation,
    CreateUserMutation,
    DeleteUserMutation,
)
from app.grafql_api.types import UserType, DocumentType
from app.models import Documents

User = get_user_model()


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_username = graphene.Field(
        UserType,
        username=graphene.String(required=True)
    )
    all_documents = graphene.List(
        DocumentType,
        first=graphene.Int(),
        offset=graphene.Int(),
        order_by=graphene.List(of_type=graphene.String),
    )
    document_by_id = graphene.Field(
        DocumentType,
        id=graphene.String(required=True)
    )

    @login_required
    def resolve_all_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @login_required
    def resolve_all_documents(
        self, info, first=None, offset=None, order_by=None, **kwargs
    ):
        qs = Documents.objects.order_by("pk")
        if offset:
            qs = qs[offset:]
        if first:
            qs = qs[:first]
        if order_by:
            qs = Documents.objects.order_by(*order_by)
        return qs

    @login_required
    def resolve_document_by_id(self, info, id):
        try:
            return Documents.objects.get(pk=id)
        except Documents.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    update_user = UpdateUserMutation.Field()
    create_user = CreateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    upload_document = UploadDocumentMutation.Field()
    delete_document = DeleteDocumentMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
