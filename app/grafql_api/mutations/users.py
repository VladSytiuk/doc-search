import graphene
from graphql_jwt.decorators import login_required

from django.contrib.auth import get_user_model

from app.grafql_api.types import UserType, CreateUserType


User = get_user_model()


class UpdateProfileMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = User.objects.get(pk=info.context.user.pk)
        for prop in kwargs:
            setattr(user, prop, kwargs[prop])
        user.save()
        return UpdateProfileMutation(user=user)


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(CreateUserType)

    @classmethod
    def mutate(cls, root, info, username, email, password, first_name="", last_name=""):
        user = User.objects.create_user(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.is_active = True
        user.save()
        return CreateUserMutation(user=user)


class ChangePasswordMutation(graphene.Mutation):
    class Arguments:
        old_password = graphene.String()
        new_password = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, old_password, new_password):
        user = User.objects.get(pk=info.context.user.pk)
        if not user.check_password(old_password):
            raise Exception("Old password is incorrect")
        user.set_password(new_password)
        user.save()
        return UpdateProfileMutation(user=user)


class DeleteProfileMutation(graphene.Mutation):
    class Arguments:
        password = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, password):
        user = User.objects.get(pk=info.context.user.pk)
        if not user.check_password(password):
            raise Exception("Password is incorrect")
        user.delete()
