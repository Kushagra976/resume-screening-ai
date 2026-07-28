Resume Screening AI
===================

Resume Screening AI is a FastAPI-based web app that helps rank candidate
resumes against a job description. Users can upload PDF resumes, paste a role
description, and receive ranked matches with extracted contact metadata.

Live App
--------

https://resume-screening-ai-production-33dc.up.railway.app/app/

What It Does
------------

- Uploads and indexes PDF resumes.
- Extracts resume text with PyMuPDF.
- Cleans and normalizes resume text before processing.
- Extracts candidate metadata such as email, phone, GitHub, and LinkedIn.
- Generates resume and job-description embeddings.
- Stores embeddings in a FAISS vector index.
- Ranks resumes by semantic similarity to the job description.
- Serves a browser frontend directly from the FastAPI backend.

Tech Stack
----------

- **Backend:** FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **PDF parsing:** PyMuPDF
- **Embeddings:** Sentence Transformers with a local fallback vectorizer
- **Vector search:** FAISS
- **Data validation:** Pydantic
- **Deployment:** Docker on Railway

Project Structure
-----------------

```text
resume-screening-ai/
|-- src/
|   |-- api/              # FastAPI app, routes, schemas, dependencies
|   |-- embeddings/       # Embedding model wrapper and fallback logic
|   |-- frontend/         # Static browser UI served at /app/
|   |-- indexing/         # Resume indexing workflow
|   |-- metadata/         # In-memory metadata store
|   |-- parser/           # Resume metadata parsing
|   |-- pdf/              # PDF extraction and text cleaning
|   |-- rankings/         # Resume ranking service
|   `-- vector_store/     # FAISS index wrapper
|-- data/
|   `-- resumes/          # Uploaded PDF resumes
|-- Dockerfile
|-- railway.json
|-- requirements.txt
`-- README.md
```

How It Works
------------

1. A user uploads one or more PDF resumes through the frontend.
2. The backend saves each PDF to `data/resumes`.
3. The PDF text is extracted and cleaned.
4. Candidate metadata is parsed from the resume text.
5. The cleaned resume text is converted into an embedding.
6. The embedding is stored in FAISS, and metadata is stored alongside it.
7. When a job description is submitted, it is embedded and searched against the
   FAISS index.
8. The API returns the closest matching resumes with similarity scores.

Run Locally
-----------

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the app:

```powershell
uvicorn src.api.main:app --reload
```

Open the frontend:

```text
http://127.0.0.1:8000/app/
```

API Endpoints
-------------

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Checks whether the API is running. |
| `GET` | `/stats` | Returns indexed resume count, embedding dimension, and model name. |
| `POST` | `/resume` | Uploads and indexes a PDF resume. |
| `POST` | `/rank` | Ranks indexed resumes against a job description. |

Example ranking request:

```json
{
  "job_description": "We need a Python backend engineer with FastAPI experience.",
  "top_k": 5
}
```

Example ranking response:

```json
{
  "matches": [
    {
      "score": 0.82,
      "metadata": {
        "email": "candidate@example.com",
        "phone": "+1 555 0100",
        "github": "https://github.com/candidate",
        "linkedin": "https://linkedin.com/in/candidate",
        "resume_path": "data/resumes/candidate.pdf"
      }
    }
  ]
}
```

Deployment
----------

This project is configured for Railway deployment with:

- `Dockerfile`
- `railway.json`
- `.dockerignore`

Railway provides the `PORT` environment variable automatically. The Docker
start command uses Railway's port when deployed and falls back to `8000` when
run locally.

To deploy:

1. Push this repository to GitHub.
2. Create a new Railway project.
3. Select "Deploy from GitHub repo".
4. Choose this repository.
5. Railway builds the Docker image and starts the FastAPI app.
6. Open the deployed URL at `/app/`.

Current deployment:

```text
https://resume-screening-ai-production-33dc.up.railway.app/app/
```

Important Notes
---------------

- The current vector index and metadata store are in memory.
- Existing PDFs in `data/resumes` are automatically indexed when the backend
  services start.
- On hosted platforms, uploaded files may not be durable across redeploys unless
  persistent storage is configured.
- For production usage, uploaded resumes should be stored in object storage such
  as S3, Cloudflare R2, or Railway volumes.
- The deployed app is suitable as a working demo, but it is not yet a hardened
  production system.

Future Improvements
-------------------

- Add persistent FAISS index and metadata storage.
- Add authentication for private resume uploads.
- Add candidate names and skills to parsed metadata.
- Add delete/re-index controls for uploaded resumes.
- Add job description history.
- Add downloadable ranking reports.
- Add tests for the API and ranking pipeline.
