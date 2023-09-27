import datetime

from django.core.files import File

from app.models import UserKeys, Documents
from app.tests.base import BaseTestCase
from app.tests.queries import QUESTION_QUERY


class QuestionsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_key = UserKeys.objects.create(
            user=self.user, reset_time=datetime.datetime.now(), key="secret"
        )
        self.user_key_exceeded = UserKeys.objects.create(
            user=self.user,
            reset_time=datetime.datetime.now(),
            key="secret2",
            queries_limit=10,
        )
        with open("app/tests/test_file.md", "rb") as f:
            file = File(f)
            self.document = Documents.objects.create(
                owner=self.user, document=file
            )

    def test_question_success(self):
        variables = {
            "key": self.user_key.key,
            "documentId": self.document.pk,
            "question": "my question",
        }
        response = self.query(
            QUESTION_QUERY, variables=variables, headers=self.headers
        )
        self.assertResponseNoErrors(response)

    def test_question_success_not_authenticated_fail(self):
        variables = {
            "key": self.user_key.key,
            "documentId": self.document.pk,
            "question": "my question",
        }
        response = self.query(QUESTION_QUERY, variables=variables)
        self.assertResponseHasErrors(response)

    def test_question_success_not_exceeded_key_limit_fail(self):
        variables = {
            "key": self.user_key_exceeded.key,
            "documentId": self.document.pk,
            "question": "my question",
        }
        response = self.query(
            QUESTION_QUERY, variables=variables, headers=self.headers
        )
        self.assertResponseHasErrors(response)
