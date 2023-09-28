import graphene

from graphql_jwt.decorators import login_required

from app.grafql_api.types import KeyType
from app.models import UserKeys


class KeysQuery(graphene.ObjectType):
    user_keys = graphene.List(KeyType)

    @login_required
    def resolve_user_keys(self, info):
        qs = UserKeys.objects.filter(user__pk=info.context.user.pk)
        return qs
