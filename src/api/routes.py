from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.api.dependencies import AppServices, get_services
from src.api.schemas import (
    HealthResponse,
    RankRequest,
    RankResponse,
    ResumeMatchResponse,
    ResumeMetadataResponse,
    ResumeUploadResponse,
    StatsResponse,
)
from src.config.paths import RESUMES_DIR
from src.utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
def health() -> HealthResponse:
    return HealthResponse(status="healthy")


@router.post(
    "/resume",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    services: AppServices = Depends(get_services),
) -> ResumeUploadResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename.",
        )

    if Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are supported.",
        )

    resume_path = _build_resume_path(file.filename)
    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded PDF is empty.",
        )

    resume_path.write_bytes(contents)

    logger.info(
        "Saved uploaded resume to %s",
        resume_path,
    )

    resume_id = services.resume_indexer.index_resume(
        resume_path,
    )

    return ResumeUploadResponse(
        message="Resume uploaded and indexed successfully.",
        resume_id=resume_id,
    )


@router.post(
    "/rank",
    response_model=RankResponse,
    status_code=status.HTTP_200_OK,
)
def rank_resumes(
    request: RankRequest,
    services: AppServices = Depends(get_services),
) -> RankResponse:
    matches = services.ranking_service.rank(
        job_description=request.job_description,
        top_k=request.top_k,
    )

    return RankResponse(
        matches=[
            ResumeMatchResponse(
                score=match.score,
                metadata=ResumeMetadataResponse(
                    email=match.metadata.email,
                    phone=match.metadata.phone,
                    github=match.metadata.github,
                    linkedin=match.metadata.linkedin,
                    resume_path=match.metadata.resume_path,
                ),
            )
            for match in matches
        ]
    )


@router.get(
    "/stats",
    response_model=StatsResponse,
    status_code=status.HTTP_200_OK,
)
def stats(
    services: AppServices = Depends(get_services),
) -> StatsResponse:
    return StatsResponse(
        indexed_resume_count=services.metadata_store.size,
        embedding_dimension=services.vector_index.dimension,
        model_name=services.embedding_generator.MODEL_NAME,
    )


def _build_resume_path(filename: str) -> Path:
    safe_name = Path(filename).name
    unique_name = f"{uuid4().hex}_{safe_name}"

    return RESUMES_DIR / unique_name
