from src.embeddings.generator import EmbeddingGenerator
from src.metadata.metadata_store import MetadataStore
from src.rankings.schema import ResumeMatch
from src.exceptions.exceptions import RankingServiceError
from src.utils.logger import get_logger
from src.vector_store.vector_index import VectorIndex

logger = get_logger(__name__)


class RankingService:

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_index: VectorIndex,
        metadata_store: MetadataStore,
    ):
        self.embedding_generator = embedding_generator
        self.vector_index = vector_index
        self.metadata_store = metadata_store

        logger.info("RankingService initialized.")