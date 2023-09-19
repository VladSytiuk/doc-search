import graphene

import graphql_jwt

from app.grafql_api.mutations.document import (
    UploadDocumentMutation,
    DeleteDocumentMutation,
)
from app.grafql_api.mutations.users import (
    UpdateProfileMutation,
    CreateUserMutation,
    ChangePasswordMutation,
    DeleteProfileMutation,
)
from app.grafql_api.queries import DocumentsQuery, UsersQuery


class Query(UsersQuery, DocumentsQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    update_user = UpdateProfileMutation.Field()
    create_user = CreateUserMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    upload_document = UploadDocumentMutation.Field()
    delete_document = DeleteDocumentMutation.Field()
    change_password = ChangePasswordMutation.Field()
    delete_profile = DeleteProfileMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
