from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

VECTORSTORE_PATH = Path("app/data/vectorstore/tgci_faiss")

_embeddings = OpenAIEmbeddings()

_tgci_store = FAISS.load_local(
    str(VECTORSTORE_PATH),
    _embeddings,
    allow_dangerous_deserialization=True
)

def load_tgci_knowledge() -> str:
    """
    Load TGCI conceptual knowledge (NOT for citation).
    Used only to ground evaluation logic, patterns, and style.
    """
    docs = _tgci_store.similarity_search(
        query="""
        TGCI grantsmanship principles, proposal readiness,
        organizational maturity, evaluation standards,
        grant opportunity structure, RFP components,
        alignment assessment, common pitfalls
        """,
        k=8
    )

    return "\n\n".join(doc.page_content for doc in docs)
