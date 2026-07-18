from pathlib import Path

from src.config.paths import RESUMES_DIR
from src.embeddings.generator import EmbeddingGenerator
from src.indexing.resume_indexer import ResumeIndexer
from src.metadata.metadata_store import MetadataStore
from src.parser.resume_parser import ResumeParser
from src.pdf.cleaner import TextCleaner
from src.pdf.extractor import PDFExtractor
from src.rankings.ranking_service import RankingService
from src.vector_store.vector_index import VectorIndex


SAMPLE_JOB_DESCRIPTION = """
We are hiring a Python software engineer with experience building
production backend services, REST APIs, data pipelines, vector search,
machine learning integrations, and clean, maintainable architecture.
"""


def find_resume_pdfs(resumes_dir: Path) -> list[Path]:
    return sorted(resumes_dir.glob("*.pdf"))


def build_services() -> tuple[ResumeIndexer, RankingService]:
    extractor = PDFExtractor()
    cleaner = TextCleaner()
    parser = ResumeParser()
    embedding_generator = EmbeddingGenerator()
    vector_index = VectorIndex(
        dimension=embedding_generator.model.get_sentence_embedding_dimension()
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

    return resume_indexer, ranking_service


def index_resumes(
    resume_indexer: ResumeIndexer,
    resume_paths: list[Path],
) -> None:
    for resume_path in resume_paths:
        resume_indexer.index_resume(resume_path)


def display_ranked_resumes(ranking_service: RankingService, top_k: int) -> None:
    matches = ranking_service.rank(
        job_description=SAMPLE_JOB_DESCRIPTION,
        top_k=top_k,
    )

    print("\nRanked resumes:")

    for position, match in enumerate(matches, start=1):
        metadata = match.metadata

        print(f"\n{position}. Score: {match.score:.4f}")
        print(f"   Resume path: {metadata.resume_path}")
        print(f"   Email: {metadata.email or 'N/A'}")
        print(f"   Phone: {metadata.phone or 'N/A'}")
        print(f"   GitHub: {metadata.github or 'N/A'}")
        print(f"   LinkedIn: {metadata.linkedin or 'N/A'}")


def main() -> None:
    resume_paths = find_resume_pdfs(RESUMES_DIR)

    if not resume_paths:
        print(f"No PDF resumes found in {RESUMES_DIR}")
        return

    resume_indexer, ranking_service = build_services()

    index_resumes(
        resume_indexer=resume_indexer,
        resume_paths=resume_paths,
    )

    display_ranked_resumes(
        ranking_service=ranking_service,
        top_k=len(resume_paths),
    )


if __name__ == "__main__":
    main()
