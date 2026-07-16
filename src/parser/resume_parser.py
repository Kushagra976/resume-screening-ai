import re
from pathlib import Path

from src.exceptions.exceptions import ResumeParserError
from src.parser.schema import ResumeMetadata
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ResumeParser:
    """
    Extracts structured metadata from cleaned resume text.
    """

    def __init__(self):
        logger.info("ResumeParser initialized.")

    def _extract_email(self, text: str) -> str | None:
        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        match = re.search(pattern, text)

        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> str | None:
        pattern = r"(?:\+?\d{1,3}[- ]?)?\d{10}"

        match = re.search(pattern, text)

        return match.group(0) if match else None

    def _extract_github(self, text: str) -> str | None:
        pattern = (
            r"(?:https?://)?(?:www\.)?"
            r"github\.com/[A-Za-z0-9_-]+"
        )

        match = re.search(pattern, text, re.IGNORECASE)

        return match.group(0) if match else None

    def _extract_linkedin(self, text: str) -> str | None:
        pattern = (
            r"(?:https?://)?(?:www\.)?"
            r"linkedin\.com/in/[A-Za-z0-9_-]+"
        )

        match = re.search(pattern, text, re.IGNORECASE)

        return match.group(0) if match else None

    def parse(
        self,
        text: str,
        resume_path: str | Path,
    ) -> ResumeMetadata:
        """
        Parse cleaned resume text and extract metadata.

        Args:
            text: Cleaned resume text.
            resume_path: Original resume file path.

        Returns:
            ResumeMetadata object.
        """

        try:
            logger.info("Parsing resume metadata.")

            metadata = ResumeMetadata(
                email=self._extract_email(text),
                phone=self._extract_phone(text),
                github=self._extract_github(text),
                linkedin=self._extract_linkedin(text),
                resume_path=str(resume_path),
            )

            logger.info("Resume metadata extracted successfully.")

            return metadata

        except Exception as e:
            logger.exception("Failed to parse resume metadata.")

            raise ResumeParserError(
                "Unable to parse resume metadata."
            ) from e