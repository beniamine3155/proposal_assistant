import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document


SECTION_PATTERN = re.compile(
    r"(?<=\n)([A-Z][A-Z\s]{5,}|[0-9]+\.\s+[A-Z].+)\n"
)


def split_by_structure(text: str):
    """
    Split text into logical sections using headings.
    """
    splits = SECTION_PATTERN.split(text)
    sections = []

    current_title = "GENERAL"
    buffer = ""

    for part in splits:
        if SECTION_PATTERN.match(part + "\n"):
            if buffer.strip():
                sections.append((current_title, buffer.strip()))
            current_title = part.strip()
            buffer = ""
        else:
            buffer += part

    if buffer.strip():
        sections.append((current_title, buffer.strip()))

    return sections


def semantic_chunk(section_text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=850,
        chunk_overlap=120
    )
    return splitter.split_text(section_text)


def create_chunks(text: str, source_name: str):
    chunks = []

    sections = split_by_structure(text)

    for section_title, section_body in sections:
        semantic_chunks = semantic_chunk(section_body)

        for chunk in semantic_chunks:
            chunks.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "section": section_title,
                        "source": source_name,
                        "chunk_type": classify_chunk(section_title)
                    }
                )
            )

    return chunks


def classify_chunk(section_title: str) -> str:
    title = section_title.lower()

    if "eligibility" in title:
        return "ELIGIBILITY"
    if "evaluation" in title or "measure" in title:
        return "EVALUATION"
    if "budget" in title or "finance" in title:
        return "BUDGET"
    if "mission" in title or "purpose" in title:
        return "MISSION"
    if "program" in title or "activities" in title:
        return "PROGRAM"
    if "readiness" in title or "capacity" in title:
        return "READINESS"

    return "TGCI_PRINCIPLE"
