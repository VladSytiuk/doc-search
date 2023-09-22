import graphene
from graphql_jwt.decorators import login_required

from app.assistant import assistant
from app.grafql_api.types import QuestionType
from app.models import UserKeys


class QuestionsQuery(graphene.ObjectType):
    question = graphene.Field(
        QuestionType,
        question=graphene.String(),
        document_id=graphene.Int(),
        key=graphene.String(),
        answer=graphene.String(),
    )

    @login_required
    def resolve_question(self, info, question, document_id, key):
        key = UserKeys.objects.get(key=key)
        if key.queries_limit >= 10:
            raise Exception("The limit of questions to be asked has been reached")
        username = info.context.user.username
        collection_name = assistant.get_collection_name(username)
        answer = assistant.process_question(question, collection_name, document_id)
        key.queries_limit += 1
        key.save()
        return QuestionType(
            answer=answer,
            question=question,
        )
