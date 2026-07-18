from dataclasses import dataclass

@dataclass(frozen=True)
class ResumeMetadata:
    email: str | None
    phone: str | None
    github: str | None
    linkedin: str | None
    resume_path: str