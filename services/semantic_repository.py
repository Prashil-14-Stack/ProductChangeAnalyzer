from services.embedding_service import EmbeddingService

from config.ai_config import (
    TOP_K_MATCHES,
    MIN_RETRIEVAL_SCORE
)


class SemanticRepository:

    def __init__(self):

        self.embedding = EmbeddingService()

        self.repository = []

    # =====================================================
    # Build Repository
    # =====================================================

    def build(self, documents):

        self.repository = []

        for document in documents:

            version = document["version"]

            filename = document["filename"]

            for parameter, text in document["parameters"].items():

                embedding = self.embedding.embed_passage(
                    f"Parameter: {parameter}\nDescription: {text}"
                )

                self.repository.append({

                    "version": version,

                    "filename": filename,

                    "parameter": parameter,

                    "text": text,

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

            # Only compare with target version
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

            # Remove obvious bad matches
            if similarity < MIN_RETRIEVAL_SCORE:

                continue

            candidates.append({

                "parameter": item["parameter"],

                "text": item["text"],

                "similarity": similarity,

                "version": item["version"],

                "filename": item["filename"]

            })

        # Highest similarity first
        candidates.sort(

            key=lambda x: x["similarity"],

            reverse=True

        )

        return candidates[:top_k]

    # =====================================================
    # Backward Compatibility
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

        if len(candidates) == 0:

            return {

                "parameter": None,

                "text": "",

                "similarity": 0

            }

        return candidates[0]