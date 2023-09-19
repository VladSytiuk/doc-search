import graphene

from graphql_jwt.decorators import login_required

from django.contrib.auth import get_user_model

from app.grafql_api.types import UserType
from app.utils import paginate_queryset

User = get_user_model()


class UsersQuery(graphene.ObjectType):
    all_users = graphene.List(
        UserType,
        first=graphene.Int(),
        limit=graphene.Int(),
        order_by=graphene.List(of_type=graphene.String),
    )
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))

    @login_required
    def resolve_all_users(
        self,
        info,
        first=None,
        limit=None,
        order_by=None,
    ):
        qs = User.objects.all()
        qs = paginate_queryset(qs, first, limit, order_by)
        return qs

    @login_required
    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
