from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from app.config import VECTOR_DB_PATH, EMBEDDING_MODEL, OPENAI_API_KEY

_tgci_store = None


def _load_store():
    global _tgci_store

    if _tgci_store is not None:
        return _tgci_store

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY
    )

    store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # 🔒 HARD SAFETY CHECK (never remove)
    test_dim = len(embeddings.embed_query("dimension check"))
    assert store.index.d == test_dim, (
        f"FAISS dim {store.index.d} != embedding dim {test_dim}"
    )

    _tgci_store = store
    return _tgci_store


def load_tgci_knowledge() -> str:
    """
    Load TGCI conceptual knowledge (NOT for citation).
    Used only to ground evaluation logic, patterns, and style.
    """
    store = _load_store()

    docs = store.similarity_search(
        query=(
            "TGCI grantsmanship principles, proposal readiness, "
            "organizational maturity, evaluation standards, "
            "grant opportunity structure, RFP components, "
            "alignment assessment, common pitfalls"
        ),
        k=8
    )

    return "\n\n".join(doc.page_content for doc in docs)
