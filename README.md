Resume Screening AI
===================

A FastAPI app for uploading PDF resumes, embedding them, and ranking the
indexed candidates against a job description.

Live App
--------

Open the deployed app here:

https://resume-screening-ai-production-33dc.up.railway.app/app/

Run the App
-----------

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Open `http://127.0.0.1:8000/app/` for the frontend.

Deploy on Railway
-----------------

This repository includes a `Dockerfile` and `railway.json`, so Railway can
build and run the FastAPI app directly.

1. Push the project to GitHub.
2. Create a new Railway project.
3. Choose "Deploy from GitHub repo".
4. Select this repository.
5. Railway will detect the Dockerfile and deploy the service.
6. Open `https://resume-screening-ai-production-33dc.up.railway.app/app/`.

Railway provides the `PORT` environment variable automatically. The Docker
start command uses it when present and falls back to port `8000` locally.

API Endpoints
-------------

- `GET /health` checks service health.
- `GET /stats` returns index size and embedding model details.
- `POST /resume` uploads and indexes one PDF resume.
- `POST /rank` ranks indexed resumes for a job description.

Notes
-----

The vector index and metadata store are in memory for the current server
process. Restarting the API clears uploaded resume matches until resumes are
uploaded again.

Uploaded resumes are stored on the service filesystem. On hosted platforms,
use a persistent volume or object storage before treating uploads as durable.
