import datetime

from django.contrib.auth import get_user_model
from django.core.files import File

from app.models import UserKeys, Documents
from app.tests.base import BaseTestCase
from app.tests.queries import DELETE_DOCUMENT_MUTATION, USER_DOCUMENTS_QUERY


User = get_user_model()


class DocumentsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_key = UserKeys.objects.create(
            user=self.user, reset_time=datetime.datetime.now(), key="secret"
        )
        with open("app/tests/test_file.md", "rb") as f:
            file = File(f)
            self.document = Documents.objects.create(owner=self.user, document=file)

    def test_delete_document_success(self):
        variables = {"id": self.document.pk}
        response = self.query(
            DELETE_DOCUMENT_MUTATION, variables=variables, headers=self.headers
        )
        self.assertResponseNoErrors(response)

    def test_delete_document_not_authenticated_fail(self):
        variables = {"id": self.document.pk}
        response = self.query(DELETE_DOCUMENT_MUTATION, variables=variables)
        self.assertResponseHasErrors(response)

    def test_get_user_documents_success(self):
        response = self.query(USER_DOCUMENTS_QUERY, headers=self.headers)
        self.assertResponseNoErrors(response)

    def test_get_user_documents_not_authenticated_fail(self):
        response = self.query(USER_DOCUMENTS_QUERY)
        self.assertResponseHasErrors(response)
