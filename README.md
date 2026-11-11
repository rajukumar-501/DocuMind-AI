# DocuMind AI

**Ask questions about your PDFs using Retrieval-Augmented Generation (RAG).**

DocuMind AI is a document question-answering application. It extracts text from uploaded PDFs, splits the text into chunks, creates vector embeddings, retrieves relevant passages with FAISS, and uses an OpenRouter-compatible language model to generate context-grounded answers.

## Features

- Upload and index PDF documents
- Extract PDF text and split it into overlapping chunks
- Generate embeddings with `sentence-transformers/all-MiniLM-L6-v2`
- Store and search document vectors with FAISS
- Generate answers using an OpenRouter-compatible chat model
- FastAPI backend with interactive Swagger documentation
- Streamlit user interface
- Docker support for the API

## Architecture

```text
PDF upload
    |
    v
FastAPI upload endpoint
    |
    v
PDF text extraction
    |
    v
Text chunking (1000 characters, 200 overlap)
    |
    v
Sentence-Transformers embeddings
    |
    v
FAISS vector index
    |
    v
User question --> FAISS similarity search
                         |
                         v
                  Relevant chunks
                         |
                         v
                  LLM via OpenRouter
                         |
                         v
                    Answer
```

## Technology stack

| Component | Technology |
|---|---|
| API | FastAPI, Uvicorn |
| UI | Streamlit |
| PDF extraction | PyPDF2 |
| Text splitting | LangChain |
| Embeddings | Sentence Transformers |
| Vector search | FAISS |
| LLM integration | LangChain OpenAI / OpenRouter |
| Metadata | SQLite |
| Containers | Docker, Docker Compose |

## Project structure

```text
documind-ai/
├── app/
│   ├── db/
│   │   └── metadata.py
│   ├── routes/
│   │   ├── metadata.py
│   │   ├── query.py
│   │   └── upload.py
│   ├── services/
│   │   ├── generator.py
│   │   ├── ingestion.py
│   │   └── retrieval.py
│   ├── utils/
│   │   └── pdf_parser.py
│   └── main.py
├── tests/
├── frontend.py
├── requirements.txt
├── requirements-frontend.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Requirements

- Python 3.11 recommended
- An OpenRouter API key (needed to generate answers)
- Docker and Docker Compose (optional)

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-frontend.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your own OpenRouter API key:

```env
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_MODEL=meta-llama/llama-3.3-8b-instruct:free
CORS_ORIGINS=http://localhost:8501
```

Never commit `.env` or expose your API key in screenshots, logs, or source code.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

API: http://localhost:8000
Swagger docs: http://localhost:8000/docs

### 6. Start the Streamlit frontend

Open a second terminal, activate the same virtual environment, then run:

```bash
streamlit run frontend.py
```

Frontend: http://localhost:8501

To use a remotely hosted API, set `API_URL` in the frontend environment to that API's base URL.

## Run with Docker

Create your `.env` file first, then:

```bash
docker compose up --build
```

The API will be available at http://localhost:8000. The Docker Compose configuration persists vector indexes and metadata in named volumes.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | API health/welcome response |
| `POST` | `/upload/` | Upload and index a PDF |
| `POST` | `/query/` | Ask a question about an indexed PDF |
| `GET` | `/upload/metadata/` | List uploaded document metadata |

### Upload example

```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "file=@sample.pdf"
```

### Query example

```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"document_id":"YOUR_DOCUMENT_ID","question":"Summarize the main points"}'
```

## Notes and limitations

- The current implementation handles text-based PDFs. Scanned PDFs may require an OCR step.
- The upload endpoint currently enforces a 10 MB file-size limit.
- The FAISS index is stored locally; this is suitable for a demo or single-instance deployment, not a multi-replica production system.
- FAISS index loading uses LangChain's dangerous deserialization option. Only load index files created and controlled by this application. Do not accept user-supplied index files.
- The model name is configurable through `OPENAI_MODEL`; availability and pricing depend on the provider.

## Tests

Run:

```bash
pytest -q
```

Add or update tests for PDF validation, ingestion, retrieval, and API error cases before treating this as production-ready.

## Roadmap

- [ ] Add OCR support for scanned PDFs
- [ ] Return source page numbers and citations with answers
- [ ] Add document deletion and index cleanup
- [ ] Add authentication and per-user document isolation
- [ ] Add automated tests with mocked embedding and LLM services
- [ ] Add deployment instructions and a public demo link

## License

Choose and add a license before accepting reuse or contributions. If you want others to freely use and modify the project, consider the MIT License.
