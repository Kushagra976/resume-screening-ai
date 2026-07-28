from dataclasses import dataclass
from functools import lru_cache

from src.embeddings.generator import EmbeddingGenerator
from src.indexing.resume_indexer import ResumeIndexer
from src.metadata.metadata_store import MetadataStore
from src.parser.resume_parser import ResumeParser
from src.pdf.cleaner import TextCleaner
from src.pdf.extractor import PDFExtractor
from src.config.paths import RESUMES_DIR
from src.rankings.ranking_service import RankingService
from src.utils.logger import get_logger
from src.vector_store.vector_index import VectorIndex


logger = get_logger(__name__)


@dataclass(frozen=True)
class AppServices:
    resume_indexer: ResumeIndexer
    ranking_service: RankingService
    embedding_generator: EmbeddingGenerator
    vector_index: VectorIndex
    metadata_store: MetadataStore


def _get_embedding_dimension(
    embedding_generator: EmbeddingGenerator,
) -> int:
    model = embedding_generator.model

    if hasattr(model, "get_embedding_dimension"):
        return model.get_embedding_dimension()

    return model.get_sentence_embedding_dimension()


def _index_existing_resumes(
    resume_indexer: ResumeIndexer,
) -> None:
    resume_paths = sorted(RESUMES_DIR.glob("*.pdf"))

    if not resume_paths:
        logger.info("No existing resumes found to index.")
        return

    logger.info("Indexing %d existing resume PDFs.", len(resume_paths))

    indexed_count = 0

    for resume_path in resume_paths:
        try:
            resume_indexer.index_resume(resume_path)
            indexed_count += 1
        except Exception:
            logger.exception(
                "Skipping existing resume that could not be indexed: %s",
                resume_path,
            )

    logger.info("Indexed %d existing resume PDFs.", indexed_count)


@lru_cache(maxsize=1)
def get_services() -> AppServices:
    extractor = PDFExtractor()
    cleaner = TextCleaner()
    parser = ResumeParser()
    embedding_generator = EmbeddingGenerator()
    vector_index = VectorIndex(
        dimension=_get_embedding_dimension(embedding_generator)
    )
    metadata_store = MetadataStore()

    resume_indexer = ResumeIndexer(
        extractor=extractor,
        cleaner=cleaner,
        parser=parser,
        embedding_generator=embedding_generator,
        vector_index=vector_index,
        metadata_store=metadata_store,
    )

    ranking_service = RankingService(
        embedding_generator=embedding_generator,
        vector_index=vector_index,
        metadata_store=metadata_store,
    )

    _index_existing_resumes(resume_indexer)

    return AppServices(
        resume_indexer=resume_indexer,
        ranking_service=ranking_service,
        embedding_generator=embedding_generator,
        vector_index=vector_index,
        metadata_store=metadata_store,
    )


def get_embedding_dimension(
    services: AppServices,
) -> int:
    return services.vector_index.dimension
