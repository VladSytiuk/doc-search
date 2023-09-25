from django.contrib.auth import get_user_model

from graphene_django.utils.testing import GraphQLTestCase

from graphql_jwt.shortcuts import get_token

from app.tests.queries import (
    USERS_LIST_QUERY,
    CREATE_USER_MUTATION,
    UPDATE_PROFILE_MUTATION,
    CHANGE_PASSWORD_MUTATION,
    DELETE_PROFILE_MUTATION,
    TOKEN_AUTH
)

User = get_user_model()


class UserTestCase(GraphQLTestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test", email="test@gmail.com")
        self.user.set_password("password")
        self.user.save()
        self.token = get_token(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"JWT {self.token}"}

    def test_get_users_lists_success(self):

        response = self.query(query=USERS_LIST_QUERY, headers=self.headers)
        self.assertResponseNoErrors(response)

    def test_get_users_lists_not_authenticated_fail(self):
        response = self.query(query=USERS_LIST_QUERY)
        self.assertResponseHasErrors(response)

    def test_create_user_success(self):
        user_data = {
            "username": "test_user",
            "email": "test_mail@gmail.com",
            "password": "password"
        }
        response = self.query(query=CREATE_USER_MUTATION, variables=user_data)
        self.assertResponseNoErrors(response)

    def test_create_user_with_not_unique_username_fail(self):
        user_data = {
            "username": "test",
            "email": "test_mail@gmail.com",
            "password": "password"
        }
        response = self.query(query=CREATE_USER_MUTATION, variables=user_data)
        self.assertResponseHasErrors(response)

    def test_create_user_with_not_unique_email_fail(self):
        user_data = {
            "username": "test_user123",
            "email": "test@gmail.com",
            "password": "password"
        }
        response = self.query(query=CREATE_USER_MUTATION, variables=user_data)
        self.assertResponseHasErrors(response)

    def test_update_profile_success(self):
        user_data = {
            "firstName": "updated_first_name",
            "lastName": "updated_last_name"
        }
        response = self.query(
            query=UPDATE_PROFILE_MUTATION, variables=user_data, headers=self.headers
        )
        self.assertResponseNoErrors(response)
        user = User.objects.get(username=self.user.username)
        assert user.first_name == user_data["firstName"]
        assert user.last_name == user_data["lastName"]

    def test_update_profile_not_authenticated_fail(self):
        user_data = {
            "firstName": "updated_first_name",
            "lastName": "updated_last_name"
        }
        response = self.query(query=UPDATE_PROFILE_MUTATION, variables=user_data)
        self.assertResponseHasErrors(response)

    def test_change_password_success(self):
        pass_data = {
            "oldPassword": "password",
            "newPassword": "new_password"
        }
        response = self.query(
            query=CHANGE_PASSWORD_MUTATION, variables=pass_data, headers=self.headers
        )
        self.assertResponseNoErrors(response)

    def test_change_password_not_authenticated_fail(self):
        pass_data = {
            "oldPassword": "password",
            "newPassword": "new_password"
        }
        response = self.query(
            query=CHANGE_PASSWORD_MUTATION, variables=pass_data
        )
        self.assertResponseHasErrors(response)

    def test_change_password_wrong_old_password_fail(self):
        pass_data = {
            "oldPassword": "wrong_password",
            "newPassword": "new_password"
        }
        response = self.query(
            query=CHANGE_PASSWORD_MUTATION, variables=pass_data
        )
        self.assertResponseHasErrors(response)

    def test_token_auth_success(self):
        auth_data = {
            "username": "test",
            "password": "password"
        }
        response = self.query(query=TOKEN_AUTH, variables=auth_data)
        self.assertResponseNoErrors(response)

    def test_token_auth_wrong_password_fail(self):
        auth_data = {
            "username": "test",
            "password": "wrong_password"
        }
        response = self.query(query=TOKEN_AUTH, variables=auth_data)
        self.assertResponseHasErrors(response)

    def test_delete_profile_success(self):
        pass_data = {"password": "password"}
        response = self.query(
            query=DELETE_PROFILE_MUTATION, variables=pass_data, headers=self.headers
        )
        self.assertResponseNoErrors(response)

    def test_delete_profile_not_authenticated_fail(self):
        pass_data = {"password": "password"}
        response = self.query(
            query=DELETE_PROFILE_MUTATION, variables=pass_data
        )
        self.assertResponseHasErrors(response)

    def test_delete_profile_wrong_password_fail(self):
        pass_data = {"password": "wrong_password"}
        response = self.query(
            query=DELETE_PROFILE_MUTATION, variables=pass_data, headers=self.headers
        )
        self.assertResponseHasErrors(response)
