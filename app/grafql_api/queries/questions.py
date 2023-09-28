import graphene
from graphql_jwt.decorators import login_required
from django_graphql_ratelimit import ratelimit

from app.assistant import assistant
from app.grafql_api.types import QuestionType
from app.models import UserKeys, Questions, User, Documents


class QuestionsQuery(graphene.ObjectType):
    question = graphene.Field(
        QuestionType,
        question=graphene.String(),
        document_id=graphene.Int(),
        key=graphene.String(),
        answer=graphene.String(),
    )

    @login_required
    @ratelimit(key="gql:key", rate="10/m", block=True)
    def resolve_question(self, info, question, document_id, key):
        if not UserKeys.objects.filter(key=key):
            raise Exception("Wrong key")
        username = info.context.user.username
        collection_name = assistant.get_collection_name(username)
        answer = assistant.process_question(
            question, collection_name, document_id
        )
        user = User.objects.get(pk=info.context.user.id)
        document = Documents.objects.filter(pk=document_id).first()
        Questions.objects.create(
            user=user, document=document, question=question
        )
        return QuestionType(
            answer=answer,
            question=question,
        )
