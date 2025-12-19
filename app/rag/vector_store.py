from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from app.config import VECTOR_DB_PATH, OPENAI_API_KEY, EMBEDDING_MODEL


def load_vector_store():
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY
    )

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
