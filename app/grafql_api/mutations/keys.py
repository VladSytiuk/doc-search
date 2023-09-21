import datetime

import graphene
from graphql_jwt.decorators import login_required

from cryptography.fernet import Fernet

from django.contrib.auth import get_user_model

from app.grafql_api.types import KeyType
from app.models import UserKeys


User = get_user_model()


class CreateKeyMutation(graphene.Mutation):
    key = graphene.Field(KeyType)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = User.objects.get(pk=info.context.user.pk)
        if UserKeys.objects.filter(user__pk=user.pk).count() >= 3:
            raise Exception("User can't create more then 3 keys")
        key = str(Fernet.generate_key())
        user_key = UserKeys.objects.create(
            user=user, reset_time=datetime.datetime.now(), key=key
        )
        return CreateKeyMutation(key=user_key)
