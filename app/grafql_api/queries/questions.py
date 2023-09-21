import graphene
from graphql_jwt.decorators import login_required

from app.assistant import assistant
from app.grafql_api.types import QuestionType


class QuestionsQuery(graphene.ObjectType):
    question = graphene.Field(
        QuestionType,
        question=graphene.String(),
        answer=graphene.String(),
        document_id=graphene.Int(),
    )

    @login_required
    def resolve_question(self, info, question, document_id):
        username = info.context.user.username
        collection_name = assistant.get_collection_name(username)
        answer = assistant.process_question(question, collection_name, document_id)
        return QuestionType(
            answer=answer,
            question=question,
        )
