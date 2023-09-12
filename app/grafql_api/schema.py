import graphene
from django.contrib.auth import get_user_model

from app.grafql_api.types import UserType


User = get_user_model()


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
