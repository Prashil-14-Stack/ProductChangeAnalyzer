from services.embedding_service import EmbeddingService


class DescriptionMatcher:

    def __init__(self):

        self.embedding = EmbeddingService()

    def compare(

        self,

        source_text,

        target_text

    ):

        source_embedding = self.embedding.embed(

            source_text

        )

        target_embedding = self.embedding.embed(

            target_text

        )

        similarity = self.embedding.cosine_similarity(

            source_embedding,

            target_embedding

        )

        return {

            "confidence": round(

                similarity * 100,

                2

            )

        }