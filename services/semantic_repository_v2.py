from services.embedding_service import EmbeddingService

from config.ai_config import (
    TOP_K_MATCHES,
    MIN_RETRIEVAL_SCORE
)

from models.semantic_index import SemanticIndex


class SemanticRepositoryV2:

    """
    Enterprise Semantic Repository

    Stores SemanticIndex objects for
    semantic comparison.
    """

    def __init__(self):

        self.embedding = EmbeddingService()

        self.repository = []

    # =====================================================
    # Build Repository
    # =====================================================

    def build(self, documents):

        self.repository.clear()

        for document in documents:

            for parameter in document.parameters:

                embedding = self.embedding.embed_passage(

                    f"Parameter: {parameter.name}\n"

                    f"Description: {parameter.value}"

                )

                semantic_index = SemanticIndex(

                    document=document,

                    parameter=parameter,

                    embedding=embedding

                )

                self.repository.append(

                    semantic_index

                )

    # =====================================================
    # Find Candidates
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

        for semantic_index in self.repository:

            if semantic_index.version != target_version:

                continue

            similarity = self.embedding.cosine_similarity(

                source_embedding,

                semantic_index.embedding

            )

            similarity = round(

                similarity * 100,

                2

            )

            if similarity < MIN_RETRIEVAL_SCORE:

                continue

            candidates.append({

                "index": semantic_index,

                "similarity": similarity

            })

        candidates.sort(

            key=lambda x: x["similarity"],

            reverse=True

        )

        return candidates[:top_k]