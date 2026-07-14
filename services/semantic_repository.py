from services.embedding_service import EmbeddingService

from config.ai_config import (
    TOP_K_MATCHES,
    MIN_RETRIEVAL_SCORE
)


class SemanticRepository:
    """
    Stable Semantic Repository (DOCX Pipeline)

    Stores semantic embeddings for dictionary-based
    parameters extracted by WordReader.
    """

    def __init__(self):

        self.embedding = EmbeddingService()

        self.repository = []

    # =====================================================
    # Build Repository
    # =====================================================

    def build(self, documents):

        self.repository = []

        for document in documents:

            for parameter, description in document["parameters"].items():

                embedding = self.embedding.embed_passage(

                    f"Parameter: {parameter}\n"

                    f"Description: {description}"

                )

                self.repository.append({

                    "version": document["version"],

                    "filename": document["filename"],

                    "parameter": parameter,

                    "text": description,

                    "embedding": embedding

                })

        return self.repository

    # =====================================================
    # Retrieve Top-K Candidates
    # =====================================================

    def find_candidates(

        self,

        source_parameter,

        source_version,

        target_version,

        top_k=TOP_K_MATCHES

    ):

        source_embedding = self.embedding.embed_query(

            source_parameter

        )

        candidates = []

        for item in self.repository:

            if item["version"] != target_version:

                continue

            similarity = self.embedding.cosine_similarity(

                source_embedding,

                item["embedding"]

            )

            similarity = round(

                similarity * 100,

                2

            )

            if similarity < MIN_RETRIEVAL_SCORE:

                continue

            candidates.append({

                "parameter": item["parameter"],

                "text": item["text"],

                "version": item["version"],

                "filename": item["filename"],

                "similarity": similarity

            })

        candidates.sort(

            key=lambda x: x["similarity"],

            reverse=True

        )

        return candidates[:top_k]

    # =====================================================
    # Retrieve Best Candidate
    # =====================================================

    def find_best_match(

        self,

        source_parameter,

        source_version,

        target_version

    ):

        candidates = self.find_candidates(

            source_parameter,

            source_version,

            target_version,

            top_k=1

        )

        if not candidates:

            return None

        return candidates[0]