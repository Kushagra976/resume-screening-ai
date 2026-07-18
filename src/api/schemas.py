from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class ResumeUploadResponse(BaseModel):
    message: str
    resume_id: int


class RankRequest(BaseModel):
    job_description: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1)


class ResumeMetadataResponse(BaseModel):
    email: str | None
    phone: str | None
    github: str | None
    linkedin: str | None
    resume_path: str


class ResumeMatchResponse(BaseModel):
    score: float
    metadata: ResumeMetadataResponse


class RankResponse(BaseModel):
    matches: list[ResumeMatchResponse]


class StatsResponse(BaseModel):
    indexed_resume_count: int
    embedding_dimension: int
    model_name: str


class ErrorResponse(BaseModel):
    detail: str
