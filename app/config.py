import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GRANT_API_KEY = os.getenv("GRANT_API_KEY")
GRANT_API_URL = os.getenv("GRANT_API_URL")

SOURCE_DIR = "app/data/tgci_sources"
VECTOR_DB_PATH = "app/data/vectorstore/tgci_faiss"

EMBEDDING_MODEL = "text-embedding-3-large"

