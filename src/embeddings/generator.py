from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

from src.exceptions.exceptions import EmbeddingGenerationError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LocalHashingEmbeddingModel:
    """
    Offline fallback model with the same small interface used by this app.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectorizer = HashingVectorizer(
            n_features=dimension,
            alternate_sign=False,
            norm="l2",
        )

    def get_embedding_dimension(self) -> int:
        return self.dimension

    def encode(
        self,
        text: str,
        convert_to_numpy: bool = True,
        normalize_embeddings: bool = True,
    ) -> np.ndarray:
        embedding = self.vectorizer.transform([text]).toarray()[0]
        return np.asarray(embedding, dtype=np.float32)


class EmbeddingGenerator:
    """
    Generates semantic embeddings from text using a Sentence Transformer model.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"
    FALLBACK_MODEL_NAME = "local-hashing-vectorizer"

    def __init__(self):
        """
        Load the embedding model once during initialization.
        """
        self.model_name = self.MODEL_NAME

        logger.info("Loading embedding model: %s", self.MODEL_NAME)

        try:
            self.model = SentenceTransformer(
                self.MODEL_NAME,
                local_files_only=True,
            )
            logger.info("Embedding model loaded successfully.")
        except Exception as exc:
            logger.warning(
                "Embedding model could not be loaded. Using offline fallback."
                " Reason: %s",
                exc,
            )
            self.model = LocalHashingEmbeddingModel()
            self.model_name = self.FALLBACK_MODEL_NAME

    def generate(self, text: str) -> np.ndarray:
        """
        Generate an embedding for the given text.

        Args:
            text: Cleaned text.

        Returns:
            A NumPy array representing the embedding.
        """

        if not text.strip():
            raise EmbeddingGenerationError(
                "Cannot generate embedding from empty text."
            )

        try:
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )

            logger.info("Embedding generated successfully.")

            return embedding

        except Exception as e:
            logger.exception("Embedding generation failed.")

            raise EmbeddingGenerationError(
                "Failed to generate embedding."
            ) from e
