from dataclasses import dataclass
from functools import lru_cache

from src.embeddings.generator import EmbeddingGenerator
from src.indexing.resume_indexer import ResumeIndexer
from src.metadata.metadata_store import MetadataStore
from src.parser.resume_parser import ResumeParser
from src.pdf.cleaner import TextCleaner
from src.pdf.extractor import PDFExtractor
from src.rankings.ranking_service import RankingService
from src.vector_store.vector_index import VectorIndex


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
