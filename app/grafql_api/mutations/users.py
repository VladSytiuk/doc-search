import graphene
from graphql_jwt.decorators import login_required

from django.contrib.auth import get_user_model

from app.grafql_api.types import UserType, CreateUserType


User = get_user_model()


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, username, email, id):
        user = User.objects.get(id=id)
        user.username = username
        user.email = email
        user.save()
        return UpdateUserMutation(user=user)


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(CreateUserType)

    @classmethod
    def mutate(cls, root, info, username, email, password):
        user = User.objects.create_user(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_active = True
        user.save()
        return CreateUserMutation(user=user)


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        user = User.objects.get(pk=id)
        user.delete()
