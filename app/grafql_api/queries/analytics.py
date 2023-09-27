import graphene
from django.db.models import Count

from app.grafql_api.types import AnalyticsUsersActivityType
from graphql_jwt.decorators import login_required

from app.models import User


class AnalyticsQuery(graphene.ObjectType):
    top_users_activity = graphene.List(AnalyticsUsersActivityType)

    @login_required
    def resolve_top_users_activity(self, info):
        qs = (
            User.objects.all()
            .annotate(documents_amount=Count("documents", distinct=True))
            .annotate(questions_amount=Count("questions", distinct=True))
            .order_by("-documents_amount", "-questions_amount")
        )
        return qs
