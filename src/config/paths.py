
from pathlib import Path


# Project Root


PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Data Directories


DATA_DIR = PROJECT_ROOT / "data"

RESUMES_DIR = DATA_DIR / "resumes"

JOBS_DIR = DATA_DIR / "jobs"

PROCESSED_DIR = DATA_DIR / "processed"


# Logs

LOG_DIR = PROJECT_ROOT / "logs"

# Models

MODELS_DIR = PROJECT_ROOT / "models"


# Create required directories automatically

for directory in (
    DATA_DIR,
    RESUMES_DIR,
    JOBS_DIR,
    PROCESSED_DIR,
    LOG_DIR,
    MODELS_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)