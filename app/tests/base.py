from django.contrib.auth import get_user_model

from graphene_django.utils import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

User = get_user_model()


class BaseTestCase(GraphQLTestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", email="test@gmail.com")
        self.user.set_password("password")
        self.user.save()
        self.token = get_token(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"JWT {self.token}"}
        self.admin_user = User.objects.create(
            username="test_admin",
            email="test_admin@gmail.com",
            is_superuser=True
        )
        self.admin_user.set_password("password")
        self.admin_user.save()
        self.admin_token = get_token(self.admin_user)
        self.admin_headers = {"HTTP_AUTHORIZATION": f"JWT {self.admin_token}"}
