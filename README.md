Resume Screening AI
===================

A FastAPI app for uploading PDF resumes, embedding them, and ranking the
indexed candidates against a job description.

Run the App
-----------

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Open `http://127.0.0.1:8000/app/` for the frontend.

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
