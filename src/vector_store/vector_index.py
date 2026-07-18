from pathlib import Path

import faiss
import numpy as np

from src.exceptions.exceptions import VectorIndexError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VectorIndex:
    """
    Wrapper around a FAISS index for storing and searching
    normalized embedding vectors.
    """

    def __init__(self, dimension: int):
        """
        Initialize an empty FAISS index.

        Args:
            dimension: Embedding dimension.
        """

        self.dimension = dimension
        self._index = faiss.IndexFlatIP(dimension)

        logger.info(
            "Initialized FAISS IndexFlatIP with dimension %d",
            dimension,
        )

    def add(
        self,
        embeddings: np.ndarray,
    ) -> list[int]:
        """
        Add one or more embeddings to the index.

        Args:
            embeddings:
                Shape (dimension,) or (N, dimension)

        Returns:
            List of assigned vector IDs.
        """

        try:

            embeddings = np.asarray(
                embeddings,
                dtype=np.float32,
            )

            if embeddings.ndim == 1:
                embeddings = embeddings.reshape(1, -1)

            if embeddings.shape[1] != self.dimension:
                raise VectorIndexError(
                    f"Expected embedding dimension "
                    f"{self.dimension}, got "
                    f"{embeddings.shape[1]}"
                )

            start_id = self.size

            self._index.add(embeddings)

            ids = list(
                range(
                    start_id,
                    start_id + embeddings.shape[0],
                )
            )

            logger.info(
                "Added %d embeddings to FAISS index.",
                embeddings.shape[0],
            )

            return ids

        except Exception as e:

            logger.exception(
                "Failed to add embeddings."
            )

            raise VectorIndexError(
                "Unable to add embeddings to index."
            ) from e

    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Search for the nearest vectors.

        Args:
            query_embedding:
                Shape (dimension,) or (1, dimension)

            k:
                Number of nearest neighbours.

        Returns:
            Tuple:
                (scores, indices)
        """

        try:

            if self.size == 0:
                raise VectorIndexError(
                    "Vector index is empty."
                )

            query_embedding = np.asarray(
                query_embedding,
                dtype=np.float32,
            )

            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(
                    1,
                    -1,
                )

            if query_embedding.shape[1] != self.dimension:
                raise VectorIndexError(
                    f"Expected embedding dimension "
                    f"{self.dimension}, got "
                    f"{query_embedding.shape[1]}"
                )

            scores, indices = self._index.search(
                query_embedding,
                k,
            )

            logger.info(
                "FAISS search completed."
            )

            return scores[0], indices[0]

        except Exception as e:

            logger.exception(
                "Search failed."
            )

            raise VectorIndexError(
                "Unable to search FAISS index."
            ) from e

    def save(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Save the index to disk.
        """

        try:

            file_path = Path(file_path)

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            faiss.write_index(
                self._index,
                str(file_path),
            )

            logger.info(
                "Saved FAISS index to %s",
                file_path,
            )

        except Exception as e:

            logger.exception(
                "Failed to save FAISS index."
            )

            raise VectorIndexError(
                "Unable to save index."
            ) from e

    def load(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Load an existing FAISS index.
        """

        try:

            file_path = Path(file_path)

            if not file_path.exists():
                raise VectorIndexError(
                    f"{file_path} does not exist."
                )

            self._index = faiss.read_index(
                str(file_path)
            )

            self.dimension = self._index.d

            logger.info(
                "Loaded FAISS index from %s",
                file_path,
            )

        except Exception as e:

            logger.exception(
                "Failed to load FAISS index."
            )

            raise VectorIndexError(
                "Unable to load index."
            ) from e

    @property
    def size(self) -> int:
        """
        Number of vectors currently stored.
        """

        return self._index.ntotal