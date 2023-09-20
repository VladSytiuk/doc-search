from app.assistant import assistant
from celery import shared_task


@shared_task
def store_document_in_vectorstore_task(document_id: int, username: str):
    assistant.store_document_in_vectorstore(document_id, username)
