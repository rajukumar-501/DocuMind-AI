#  RAG Pipeline API

A Retrieval-Augmented Generation (RAG) system with FastAPI, FAISS, Hugging Face Embeddings, and OpenRouter LLMs.

---

##  Features

- Upload and chunk PDF documents
- Store embeddings using FAISS
- Query documents using OpenRouter-compatible LLMs (like LLaMA-3)
- Fully containerized with Docker Compose
- Easily deployable on local or cloud environments

---

##  Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-project>
```

### 2. Create `.env`
```env
your_gemini_api_key_here
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

App will be available at [http://localhost:8000](http://localhost:8000)

---

##  Testing

### Run unit tests:
```bash
docker exec -it rag_api pytest tests/
```

---

##  API Usage

### Upload PDF
```http
POST /upload/
Form-Data: file = <yourfile.pdf>
```

### Query Document
```http
POST /query/
{
  "document_id": "uuid",
  "question": "What is this about?"
}
```

### Get Metadata
```http
GET /upload/metadata/
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

##  Cloud Deployment (AWS/GCP/Azure)

1. Build image:
```bash
docker build -t rag-api .
```

2. Push to registry (ECR/GCR/ACR)

3. Run on:
- AWS ECS/Fargate
- GCP Cloud Run
- Azure Container Apps

Make sure to provide environment variables (`OPENAI_API_KEY`, `OPENAI_API_BASE`) via the platform's secret/config mechanism.

---

## Switch LLM Provider

| Provider       | Key Env                 | Base URL                            | Model                        |
|----------------|--------------------------|--------------------------------------|------------------------------|
| OpenAI         | `OPENAI_API_KEY`         | *none needed*                       | `gpt-3.5-turbo`              |
| OpenRouter     | `OPENAI_API_KEY`         | `https://openrouter.ai/api/v1`     | `openrouter/meta-llama-3-8b-instruct` |
| Gemini (Google)| `GOOGLE_API_KEY`         | `via palm SDK`                     | `gemini-pro`                 |

Update `generator.py` model name accordingly.

---

##  Folder Structure
```
├── app
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── db/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

# 📄 Streamlit Frontend for RAG App

This is a simple and clean Streamlit frontend for the Retrieval-Augmented Generation (RAG) API backend. It allows users to:

- Upload PDF documents
- Ask questions about the uploaded content
- Get AI-generated answers from a connected LLM via OpenRouter

---

## 🚀 Features

- Upload `.pdf` files directly
- Automatically extracts and chunks text
- Ask questions based on document content
- LLM-powered answers (uses OpenRouter-compatible model)
- Sidebar to view uploaded document metadata

---

## 🔧 Setup & Run Locally

### 1. Make sure backend is running at:
```
http://localhost:8000
```
This is the FastAPI app with `/upload/`, `/query/`, and `/upload/metadata/` routes.

### 2. Install dependencies
```bash
pip install streamlit requests
```

### 3. Run the frontend
```bash
streamlit run frontend.py
```

Visit [http://localhost:8501](http://localhost:8501) to use the app.

---

## 📦 API Endpoints Used

- `POST /upload/` → Upload a PDF
- `POST /query/` → Ask question about PDF
- `GET /upload/metadata/` → View uploaded docs

# Panscience
# Panscience
