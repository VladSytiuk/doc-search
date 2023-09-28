import graphene

from graphql_jwt.decorators import login_required, superuser_required

from django.contrib.auth import get_user_model

from app.grafql_api.types import DocumentType
from app.models import Documents
from app.utils import paginate_queryset


User = get_user_model()


class DocumentsQuery(graphene.ObjectType):
    all_documents = graphene.List(
        DocumentType,
        first=graphene.Int(),
        limit=graphene.Int(),
        order_by=graphene.List(of_type=graphene.String),
    )
    document_by_id = graphene.Field(
        DocumentType, id=graphene.String(required=True)
    )
    user_documents = graphene.List(DocumentType)

    @superuser_required
    def resolve_all_documents(
        self, info, first=None, limit=None, order_by=None, **kwargs
    ):
        qs = Documents.objects.all()
        qs = paginate_queryset(qs, first=first, limit=limit, order_by=order_by)
        return qs

    @login_required
    def resolve_document_by_id(self, info, id):
        try:
            return Documents.objects.get(pk=id)
        except Documents.DoesNotExist:
            return None

    @login_required
    def resolve_user_documents(self, info):
        qs = Documents.objects.filter(owner__pk=info.context.user.pk)
        return qs
