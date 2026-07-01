from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from config import EMBEDDING_MODEL
class EP5Service:

    """
    Enterprise E5 Embedding Service

    Responsibilities:
        • Load E5 model once
        • Generate embeddings
        • Compute cosine similarity
    """

    def __init__(self):

        from config.ai_config import EMBEDDING_MODEL

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    # ==================================================
    # Generate Embedding
    # ==================================================

    def embed(self, text):

        if text is None:
            text = ""

        return self.model.encode(

            f"query: {text}",

            convert_to_tensor=True,

            normalize_embeddings=True

        )

    # ==================================================
    # Cosine Similarity
    # ==================================================

    def cosine_similarity(

        self,

        embedding1,

        embedding2

    ):

        return cos_sim(

            embedding1,

            embedding2

        ).item()

    # ==================================================
    # Convenience Method
    # ==================================================

    def compare(

        self,

        text1,

        text2

    ):

        embedding1 = self.embed(text1)

        embedding2 = self.embed(text2)

        similarity = self.cosine_similarity(

            embedding1,

            embedding2

        )

        return round(

            similarity * 100,

            2

        )