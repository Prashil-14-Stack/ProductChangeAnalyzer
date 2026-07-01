from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from config.ai_config import EMBEDDING_MODEL


class EmbeddingService:
    """
    Enterprise Embedding Service

    Responsibilities
    ----------------
    • Load embedding model only once
    • Generate query embeddings
    • Generate passage embeddings
    • Compute cosine similarity
    """

    _model = None

    def __init__(self):

        if EmbeddingService._model is None:

            EmbeddingService._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        self.model = EmbeddingService._model

    # ==================================================
    # Query Embedding
    # Used when searching the repository
    # ==================================================

    def embed_query(self, text):

        if text is None:
            text = ""

        return self.model.encode(

            f"query: {text}",

            convert_to_tensor=True,

            normalize_embeddings=True

        )

    # ==================================================
    # Passage Embedding
    # Used when building the repository
    # ==================================================

    def embed_passage(self, text):

        if text is None:
            text = ""

        return self.model.encode(

            f"passage: {text}",

            convert_to_tensor=True,

            normalize_embeddings=True

        )

    # ==================================================
    # Generic Embedding
    # Backward compatibility
    # ==================================================

    def embed(self, text):

        return self.embed_query(text)

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
    # Compare Two Texts
    # ==================================================

    def compare(

        self,

        text1,

        text2

    ):

        embedding1 = self.embed_query(text1)

        embedding2 = self.embed_query(text2)

        similarity = self.cosine_similarity(

            embedding1,

            embedding2

        )

        return round(

            similarity * 100,

            2

        )