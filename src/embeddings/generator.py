from sentence_transformers import SentenceTransformer
import numpy as np

from src.exceptions.exceptions import EmbeddingGenerationError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates semantic embeddings from text using a Sentence Transformer model.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        """
        Load the embedding model once during initialization.
        """
        logger.info("Loading embedding model: %s", self.MODEL_NAME)

        self.model = SentenceTransformer(self.MODEL_NAME)

        logger.info("Embedding model loaded successfully.")

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