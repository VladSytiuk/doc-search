import graphene
from django.contrib.auth import get_user_model
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required

from app.models import Documents


User = get_user_model()


class UploadDocumentMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    document_id = graphene.ID()

    @login_required
    def mutate(self, info, file, **kwargs):
        file_name = file.__dict__["_name"]
        if Documents.objects.filter(title=file_name).exists():
            raise Exception("Document already exists")
        user = User.objects.get(pk=info.context.user.pk)
        document = Documents.objects.create(
            document=file,
            title=file_name,
            owner=user
        )
        return UploadDocumentMutation(document_id=document.pk)
