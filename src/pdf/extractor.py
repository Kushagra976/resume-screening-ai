from pathlib import Path

import fitz

from src.exceptions.exceptions import (
    PDFExtractionError,
    UnsupportedFileFormatError,
)
from src.utils.logger import get_logger


logger = get_logger(__name__)


class PDFExtractor:
    """
    Service responsible for extracting text from PDF documents.
    """

    SUPPORTED_EXTENSIONS = {".pdf"}

    def extract(self, pdf_path: str | Path) -> str:
        """
        Extract text from a PDF.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text as a single string.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            UnsupportedFileFormatError:
                If the file is not a PDF.

            PDFExtractionError:
                If extraction fails.
        """

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"File not found: {pdf_path}"
            )

        if pdf_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileFormatError(
                f"Unsupported file format: {pdf_path.suffix}"
            )

        logger.info("Opening PDF: %s", pdf_path.name)

        try:

            extracted_pages = []

            with fitz.open(pdf_path) as document:

                logger.info(
                    "PDF contains %d pages",
                    len(document),
                )

                for page in document:
                    extracted_pages.append(
                        page.get_text()
                    )

            text = "\n".join(extracted_pages).strip()

            logger.info(
                "Successfully extracted text from %s",
                pdf_path.name,
            )

            return text

        except Exception as e:

            logger.exception(
                "PDF extraction failed."
            )

            raise PDFExtractionError(
                f"Failed to extract text from {pdf_path.name}"
            ) from e