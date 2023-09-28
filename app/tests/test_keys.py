from django.contrib.auth import get_user_model

from app.tests.base import BaseTestCase
from app.tests.queries import CREATE_KEY_MUTATION, USER_KEYS_QUERY


User = get_user_model()


class UserTestCase(BaseTestCase):
    def test_create_key_success(self):
        response = self.query(CREATE_KEY_MUTATION, headers=self.headers)
        self.assertResponseNoErrors(response)

    def test_create_key_not_authenticated_fail(self):
        response = self.query(CREATE_KEY_MUTATION)
        self.assertResponseHasErrors(response)

    def test_create_key_limit_exceeded_fail(self):
        for i in range(3):
            self.query(CREATE_KEY_MUTATION, headers=self.headers)
        response = self.query(CREATE_KEY_MUTATION, headers=self.headers)
        self.assertResponseHasErrors(response)

    def test_get_user_keys_success(self):
        response = self.query(USER_KEYS_QUERY, headers=self.headers)
        self.assertResponseNoErrors(response)

    def test_get_user_keys_not_authenticated_fail(self):
        response = self.query(USER_KEYS_QUERY)
        self.assertResponseHasErrors(response)
