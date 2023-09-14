import graphene
from graphql_jwt.decorators import login_required
import graphql_jwt
from django.contrib.auth import get_user_model

from app.grafql_api.mutations.document import UploadDocumentMutation
from app.grafql_api.mutations.users import (
    UpdateUserMutation,
    CreateUserMutation,
    DeleteUserMutation,
)
from app.grafql_api.types import UserType


User = get_user_model()


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))

    @login_required
    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    update_user = UpdateUserMutation.Field()
    create_user = CreateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    upload_document = UploadDocumentMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
