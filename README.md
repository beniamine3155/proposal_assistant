# TGCI Proposal Assistant

A comprehensive AI-powered FastAPI application designed to assist organizations in grant proposal development, opportunity identification, and readiness assessment. The system leverages LLMs (OpenAI) and RAG (Retrieval-Augmented Generation) to provide intelligent grant matching, proposal generation, and organizational profiling.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies](#technologies)
- [Services](#services)

## 🎯 Overview

The TGCI Proposal Assistant is a multi-module application that helps organizations:
- Analyze their grant readiness and organizational profile
- Discover grant opportunities aligned with their mission
- Generate customized grant proposals
- Create Letters of Intent (LOI)
- Leverage a knowledge base powered by vector embeddings

The application uses FastAPI for the REST API, LangChain for RAG capabilities, and OpenAI for intelligent content generation.

## ✨ Features

- **Grant Readiness Analysis**: Analyze organizations with or without website information
- **Grant Opportunity Discovery**: Find and recommend matching grant opportunities
- **Intelligent Grant Generation**: Auto-generate new grant opportunities based on organization profile
- **Proposal Generation**: Create complete grant proposals with AI assistance
- **Letter of Intent (LOI) Creation**: Generate LOI documents from grant opportunities
- **RAG-Based Knowledge System**: Vector embeddings (FAISS) for semantic search and context retrieval
- **Multi-Format Support**: Handle PDF, DOCX, and text inputs
- **Session Management**: Track multiple organization analysis sessions

## 📁 Project Structure

```
proposal_assistant/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── template.py                        # Template utilities
├── app/                               # Main application package
│   ├── __init__.py
│   ├── config.py                      # Configuration and environment variables
│   ├── main.py                        # FastAPI application entry point
│   ├── api/                           # API endpoints
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── onboarding.py      # Organization analysis endpoints
│   │           ├── grant_opportunity.py # Grant opportunity endpoints
│   │           ├── grant_generator.py  # Grant generation endpoints
│   │           ├── loi.py              # Letter of Intent endpoints
│   │           └── proposal.py         # Proposal generation endpoints
│   ├── data/                          # Data storage and management
│   │   ├── grant_store.py             # Grant data persistence
│   │   ├── org_store.py               # Organization profile storage
│   │   ├── tgci_sources/              # Raw grant source documents
│   │   └── vectorstore/
│   │       └── tgci_faiss/            # FAISS vector database index
│   ├── model/                         # Data models
│   │   └── response.py                # Response model definitions
│   ├── rag/                           # Retrieval-Augmented Generation
│   │   ├── chunker.py                 # Document chunking logic
│   │   ├── ingest.py                  # Data ingestion pipeline
│   │   └── vector_store.py            # Vector store operations
│   ├── schemas/                       # Pydantic request/response schemas
│   │   ├── grant_fetch.py             # Grant fetch request/response schemas
│   │   ├── grant_opportunity.py       # Grant opportunity schemas
│   │   ├── loi.py                     # LOI schemas
│   │   ├── onboarding.py              # Onboarding/analysis schemas
│   │   ├── proposal.py                # Proposal schemas
│   │   └── request.py                 # Common request schemas
│   ├── services/                      # Business logic and external integrations
│   │   ├── llm_service.py             # OpenAI LLM interactions
│   │   ├── grant_api_service.py       # External grant API integration
│   │   ├── grant_generator_service.py # Grant generation logic
│   │   ├── grant_opportunity_service.py # Grant opportunity matching
│   │   ├── grant_readiness_service.py # Organization readiness analysis
│   │   ├── loi_service.py             # LOI generation
│   │   ├── proposal_service.py        # Proposal generation
│   │   ├── tgci_knowledge.py          # TGCI knowledge base utilities
│   │   └── website_scraper.py         # Web scraping for organization info
│   └── utils/                         # Utility functions

```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Grant API credentials (if using external grant API)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd proposal_assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (see Configuration section)

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# External Grant API (optional)
GRANT_API_KEY=your_grant_api_key
GRANT_API_URL=https://api.grantapi.com

# File paths (automatically configured)
SOURCE_DIR=app/data/tgci_sources
VECTOR_DB_PATH=app/data/vectorstore/tgci_faiss

# LLM Model Configuration
EMBEDDING_MODEL=text-embedding-3-large
```

**Key Configuration Variables:**
- `OPENAI_API_KEY`: Required for LLM and embedding operations
- `GRANT_API_KEY` & `GRANT_API_URL`: Optional, for fetching external grant data
- `EMBEDDING_MODEL`: OpenAI embedding model for vector generation (default: text-embedding-3-large)
- `VECTOR_DB_PATH`: Path to the FAISS vector database

## 🎮 Usage

### Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API**
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/

### Example Workflow

1. **Analyze Organization** (Onboarding)
   ```bash
   POST /onboarding/analyze/with-website
   # or
   POST /onboarding/analyze/without-website
   ```

2. **Generate Grant Opportunities**
   ```bash
   POST /grant-generator/generate
   ```

3. **Find Matching Opportunities**
   ```bash
   POST /grant-opportunity/find
   ```

4. **Generate Proposal**
   ```bash
   POST /proposal/generate
   ```

## 🔗 API Endpoints

### Onboarding (Organization Analysis)
- `POST /onboarding/analyze/with-website` - Analyze organization using website
- `POST /onboarding/analyze/without-website` - Analyze organization using manual input

### Grant Generator
- `POST /grant-generator/generate` - Generate new grant opportunities

### Grant Opportunity
- `POST /grant-opportunity/find` - Find matching grant opportunities

### Letter of Intent (LOI)
- `POST /loi/generate` - Generate LOI from grant opportunity

### Proposal
- `POST /proposal/generate` - Generate complete grant proposal

## 💻 Technologies

### Framework & Web
- **FastAPI** - Modern Python web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI

### AI & LLM
- **OpenAI** - LLM (ChatGPT) for content generation and analysis
- **LangChain** - Framework for LLM applications and RAG
- **LangGraph** - Graph-based orchestration for complex workflows

### Vector & Search
- **FAISS** - Facebook AI Similarity Search for vector similarity
- **LangChain Community** - Community integrations including vector stores

### Data Processing
- **Pydantic** - Data validation and serialization
- **pdfplumber** - PDF extraction and parsing
- **python-docx** - DOCX file handling
- **BeautifulSoup4** - HTML parsing
- **trafilatura** - Web content extraction
- **Requests** - HTTP library

### Environment
- **python-dotenv** - Environment variable management

## 🔧 Services

### Core Services

#### **llm_service.py**
Handles all OpenAI LLM interactions. Features:
- Organization profile extraction
- Content generation and refinement
- TGCI knowledge base integration
- Prompt management and optimization

#### **grant_generator_service.py**
Generates new grant opportunities based on organization profiles.
- Analyzes alignment with sample grants
- Creates realistic, funder-driven opportunities
- Validates focus field categorization

#### **grant_opportunity_service.py**
Matches organizations with suitable grant opportunities.
- Semantic search via FAISS vectors
- Relevance scoring
- Opportunity filtering and ranking

#### **grant_readiness_service.py**
Analyzes organizational grant readiness.
- Website scraping for org information
- Profile construction from user input
- Readiness scoring and recommendations

#### **proposal_service.py**
Generates complete grant proposals.
- Multi-section proposal generation
- Session-based tracking
- Formatted output generation

#### **loi_service.py**
Creates Letters of Intent.
- LOI structure and formatting
- Grant-specific customization

#### **grant_api_service.py**
External grant database integration.
- API communication
- Grant data fetching and normalization

#### **tgci_knowledge.py**
TGCI-specific knowledge base utilities.
- Knowledge loading and caching
- Context retrieval

#### **website_scraper.py**
Web scraping utilities.
- Organization website content extraction
- Information structuring

### Data Management

#### **grant_store.py**
Persistent storage for grant data.

#### **org_store.py**
Organization profile storage and retrieval.

### RAG (Retrieval-Augmented Generation)

#### **vector_store.py**
FAISS vector store operations.
- Load pre-built indexes
- Semantic search

#### **chunker.py**
Document chunking strategies.
- Text segmentation
- Context preservation

#### **ingest.py**
Data ingestion pipeline.
- Document processing
- Vector generation
- Index updates

## 📊 Data Storage

- **tgci_sources/**: Raw grant documents and source materials
- **vectorstore/tgci_faiss/**: FAISS vector database
  - `index.faiss`: Binary vector index for semantic search

## 📝 Request/Response Schemas (Pydantic Models)

All API requests and responses are validated using Pydantic schemas located in `app/schemas/`:
- `onboarding.py` - Organization analysis requests/responses
- `grant_opportunity.py` - Grant opportunity payloads
- `grant_fetch.py` - Grant fetching specifications
- `proposal.py` - Proposal generation requests/responses
- `loi.py` - LOI generation payloads
- `request.py` - Common request structures

## 🔐 Security & Best Practices

- Environment variables for sensitive credentials
- Input validation via Pydantic
- Error handling with appropriate HTTP status codes
- Async operations for scalability

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

