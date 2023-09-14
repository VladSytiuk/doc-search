import graphene
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required

from app.models import Documents


class UploadDocumentMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    document_id = graphene.ID()

    @login_required
    def mutate(self, info, file, **kwargs):
        document = Documents.objects.create(document=file)

        return UploadDocumentMutation(document_id=document.pk)
