from dataclasses import dataclass

from src.parser.schema import ResumeMetadata


@dataclass(frozen=True)
class ResumeMatch:
    score: float
    metadata: ResumeMetadata