from app.config import MAX_CHARS

def chunk_text(text: str):
    chunks = []
    start = 0

    while start < len(text):
        end = start + MAX_CHARS
        chunks.append(text[start:end])
        start = end

    return chunks
