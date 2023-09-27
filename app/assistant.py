from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import (
    PyPDFium2Loader,
    UnstructuredMarkdownLoader,
)
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from app.models import Documents


TEMPLATE = """The chat bot should introduce itself as "Documents assistant".
If the chat has no answer, it should say specifically: "I don't know
please contact support by email support@doc_search.com".
Chat should look for an answer from vectorstore documents.
{context}
Question: {question}
Helpful Answer:"""


class AssistantService:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    QA_CHAIN_PROMPT = PromptTemplate.from_template(TEMPLATE)

    def process_question(
        self, question: str, collection: str, document_id: int
    ) -> str:
        document = Documents.objects.get(pk=document_id)
        document_source = self._get_document_url(document)
        vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=OpenAIEmbeddings(),
            collection_name=collection,
        )
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 1, "filter": {"source": document_source}},
            ),
            chain_type_kwargs={"prompt": self.QA_CHAIN_PROMPT},
        )
        answer = qa_chain({"query": question})
        return answer["result"]

    def _load_document(self, id) -> list:
        document = Documents.objects.get(pk=id)
        document_url = self._get_document_url(document)
        extension = self._get_document_extension(document.title)
        if extension == "pdf":
            raw_document = PyPDFium2Loader(document_url).load()
        if extension == "md":
            raw_document = UnstructuredMarkdownLoader(document_url).load()
        return raw_document

    @staticmethod
    def _split_document(raw_document: list) -> list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=20
        )
        chunked_documents = text_splitter.split_documents(raw_document)
        return chunked_documents

    def store_document_in_vectorstore(
        self, document_id: int, username: str
    ) -> None:
        document = self._load_document(document_id)
        chunks = self._split_document(document)
        collection_name = self.get_collection_name(username)
        Chroma.from_documents(
            chunks,
            OpenAIEmbeddings(),
            persist_directory="./chroma_db",
            collection_name=collection_name,
        )

    @staticmethod
    def get_collection_name(username: str) -> str:
        return username + "_vectorstore"

    @staticmethod
    def _get_document_extension(title: str) -> str:
        return title.split(".")[-1].lower()

    @staticmethod
    def _get_document_url(document: Documents):
        return document.document.url[1:]


assistant = AssistantService()
