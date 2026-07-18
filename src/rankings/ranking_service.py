from src.embeddings.generator import EmbeddingGenerator
from src.exceptions.exceptions import RankingServiceError
from src.metadata.metadata_store import MetadataStore
from src.rankings.schema import ResumeMatch
from src.utils.logger import get_logger
from src.vector_store.vector_index import VectorIndex

logger = get_logger(__name__)


class RankingService:
    """
    Service responsible for ranking resumes
    against a given job description.
    """

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

    def rank(
        self,
        job_description: str,
        top_k: int = 5,
    ) -> list[ResumeMatch]:
        """
        Rank indexed resumes against a job description.

        Args:
            job_description:
                Job description text.

            top_k:
                Number of resumes to return.

        Returns:
            List of ResumeMatch objects sorted
            by similarity score.
        """

        try:

            logger.info("Ranking resumes.")

            job_embedding = (
                self.embedding_generator.generate(
                    job_description,
                )
            )

            scores, indices = (
                self.vector_index.search(
                    job_embedding,
                    top_k,
                )
            )

            matches = []

            for score, idx in zip(scores, indices):

                if idx == -1:
                    continue

                metadata = self.metadata_store.get(
                    int(idx),
                )

                matches.append(
                    ResumeMatch(
                        score=float(score),
                        metadata=metadata,
                    )
                )

            logger.info(
                "Found %d matching resumes.",
                len(matches),
            )

            return matches

        except Exception as e:

            logger.exception(
                "Resume ranking failed."
            )

            raise RankingServiceError(
                "Unable to rank resumes."
            ) from e
