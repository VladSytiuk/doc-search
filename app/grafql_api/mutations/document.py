import graphene
from graphene_file_upload.scalars import Upload

from django.contrib.auth import get_user_model

from graphql_jwt.decorators import login_required

from app.grafql_api.types import DocumentType
from app.models import Documents, UserKeys
from app.tasks import store_document_in_vectorstore_task


User = get_user_model()


class UploadDocumentMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
        key = graphene.String()

    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, file, key, **kwargs):
        file_name = file.__dict__["_name"]
        if not cls.check_document_extension(file_name):
            raise Exception("Document should be in pdf or md format")

        key = UserKeys.objects.get(key=key)
        if not cls.check_key_documents_limit(key):
            raise Exception("The limit of documents to be uploaded has been reached")

        user = User.objects.get(pk=info.context.user.pk)
        document = Documents.objects.create(document=file, title=file_name, owner=user)
        key.documents_limit += 1
        key.save()
        store_document_in_vectorstore_task.delay(document.pk, user.username)

        return UploadDocumentMutation(success=True)

    @staticmethod
    def check_document_extension(file_name: str) -> bool:
        return file_name.lower().endswith((".pdf", ".md"))

    @staticmethod
    def check_key_documents_limit(key: UserKeys) -> bool:
        return key.documents_limit < 10


class DeleteDocumentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    document = graphene.Field(DocumentType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        document = Documents.objects.get(pk=id)
        if not document.owner.pk == info.context.user.pk:
            raise Exception("You don't have permission to delete this document")
        document.delete()
