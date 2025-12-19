import os
from langchain_community.document_loaders import PyPDFLoader
from docx import Document as DocxDocument
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import (
    SOURCE_DIR,
    VECTOR_DB_PATH,
    OPENAI_API_KEY,
    EMBEDDING_MODEL
)
from app.rag.chunker import create_chunks


def load_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        return "\n".join(p.page_content for p in pages)

    if file_path.endswith(".docx"):
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    return ""


def ingest_all_sources():
    all_chunks = []

    for file in os.listdir(SOURCE_DIR):
        path = os.path.join(SOURCE_DIR, file)
        print(f"📄 Processing: {file}")

        text = load_text(path)
        chunks = create_chunks(text, source_name=file)
        all_chunks.extend(chunks)

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY
    )

    vectorstore = FAISS.from_documents(all_chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)

    print(f"\n✅ INGESTION COMPLETE")
    print(f"Total chunks stored: {len(all_chunks)}")


if __name__ == "__main__":
    ingest_all_sources()
