from pathlib import Path

from src.embeddings.generator import EmbeddingGenerator
from src.exceptions.exceptions import ResumeScreeningError
from src.metadata.metadata_store import MetadataStore
from src.parser.resume_parser import ResumeParser
from src.pdf.cleaner import TextCleaner
from src.pdf.extractor import PDFExtractor
from src.utils.logger import get_logger
from src.vector_store.vector_index import VectorIndex
from src.exceptions.exceptions import ResumeIndexerError
logger = get_logger(__name__)


class ResumeIndexer:

    def __init__(
        self,
        extractor: PDFExtractor,
        cleaner: TextCleaner,
        parser: ResumeParser,
        embedding_generator: EmbeddingGenerator,
        vector_index: VectorIndex,
        metadata_store: MetadataStore,
    ):
        self.extractor = extractor
        self.cleaner = cleaner
        self.parser = parser
        self.embedding_generator = embedding_generator
        self.vector_index = vector_index
        self.metadata_store = metadata_store

        logger.info("ResumeIndexer initialized.")

    def index_resume(
        self,
        pdf_path: str | Path,
    ) -> int:

        try:

            logger.info(
                "Indexing resume %s",
                pdf_path,
            )

            raw_text = self.extractor.extract(
                pdf_path,
            )

            cleaned_text = self.cleaner.clean(
                raw_text,
            )

            metadata = self.parser.parse(
                cleaned_text,
                pdf_path,
            )

            embedding = self.embedding_generator.generate(
                cleaned_text,
            )

            ids = self.vector_index.add(
                embedding,
            )

            self.metadata_store.add(
                ids[0],
                metadata,
            )

            logger.info(
                "Successfully indexed %s with id %d",
                pdf_path,
                ids[0],
            )

            return ids[0]

        except Exception as e:

            logger.exception(
                "Resume indexing failed."
            )

            raise ResumeIndexerError(
                "Unable to index resume."
            ) from e