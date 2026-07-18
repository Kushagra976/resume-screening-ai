from pathlib import Path
import pickle

from src.parser.schema import ResumeMetadata
from src.utils.logger import get_logger
from src.utils.exceptions import (
    MetadataStoreError,
)

logger = get_logger(__name__)


class MetadataStore:

    def __init__(self):
        self._metadata: dict[int, ResumeMetadata] = {}
        logger.info("MetadataStore initialized.")

    @property
    def size(self) -> int:
        return len(self._metadata)

    def add(
        self,
        idx: int,
        metadata: ResumeMetadata,
    ) -> None:

        if idx in self._metadata:
            raise MetadataStoreError(
                f"Metadata already exists for id {idx}"
            )

        self._metadata[idx] = metadata

        logger.info(f"Added metadata for id {idx}")

    def get(
        self,
        idx: int,
    ) -> ResumeMetadata:

        if idx not in self._metadata:
            raise MetadataStoreError(
                f"Metadata not found for id {idx}"
            )

        return self._metadata[idx]

    def delete(
        self,
        idx: int,
    ) -> None:

        if idx not in self._metadata:
            raise MetadataStoreError(
                f"Metadata not found for id {idx}"
            )

        del self._metadata[idx]

        logger.info(f"Deleted metadata for id {idx}")

    def save(
        self,
        path: str | Path,
    ) -> None:

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(path, "wb") as file:
            pickle.dump(
                self._metadata,
                file,
            )

        logger.info(f"Metadata saved to {path}")

    def load(
        self,
        path: str | Path,
    ) -> None:

        path = Path(path)

        if not path.exists():
            raise MetadataStoreError(
                f"{path} does not exist."
            )

        with open(path, "rb") as file:
            self._metadata = pickle.load(file)

        logger.info(f"Metadata loaded from {path}")