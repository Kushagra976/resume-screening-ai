"""
Custom exception hierarchy for the Resume Screening AI project.
"""


class ResumeScreeningError(Exception):
    """
    Base exception for all project-specific errors.
    """

    pass


class PDFExtractionError(ResumeScreeningError):
    """
    Raised when text extraction from a PDF fails.
    """

    pass


class UnsupportedFileFormatError(ResumeScreeningError):
    """
    Raised when an unsupported file format is provided.
    """

    pass


class EmbeddingGenerationError(ResumeScreeningError):
    """
    Raised when embedding generation fails.
    """

    pass


class VectorIndexError(ResumeScreeningError):
    """
    Raised when operations on the vector index fail.
    """

    pass


class MetadataStoreError(ResumeScreeningError):
    """
    Raised when metadata storage operations fail.
    """

    pass


class ConfigurationError(ResumeScreeningError):
    """
    Raised when the application configuration is invalid.
    """

    pass

class ResumeParserError(ResumeScreeningError):
    """Raised when resume metadata parsing fails."""
    pass

class RankingServiceError(ResumeScreeningError):
    """Raised when ranking resumes fails."""
    pass

class ResumeIndexerError(ResumeScreeningError):
    """Raised when resume indexing fails."""
    pass
