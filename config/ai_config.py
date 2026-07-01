# ==========================================
# AI Configuration
# ==========================================

# Embedding Model
EMBEDDING_MODEL = "intfloat/e5-base-v2"

# Similarity Threshold (0-100)
SIMILARITY_THRESHOLD = 85

# Return Top K Semantic Matches
TOP_K_MATCHES = 3

# Cache Embeddings
CACHE_EMBEDDINGS = True

# Enable Exact Match before Semantic Match
ENABLE_EXACT_MATCH = True

# Enable Semantic Matching
ENABLE_SEMANTIC_MATCH = True

# ----------------------------------------
# Parameter Matching
# ----------------------------------------

PARAMETER_MATCH_THRESHOLD = 90

PARAMETER_REVIEW_THRESHOLD = 80

DESCRIPTION_MATCH_THRESHOLD = 90

MIN_RETRIEVAL_SCORE = 50

LLM_PROVIDER = "MOCK"