from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

class SemanticEmbeddingMatcher:


    def __init__(self):

        print("\nLoading E5 Large Model...")

        self.model = SentenceTransformer(
            "intfloat/e5-large-v2"
        )

        print("E5 Large Model Loaded Successfully\n")

    def find_match(
            self,
            v1_parameter,
            v1_description,
            v2_data):

        # =====================================
        # V1 PARAMETER EMBEDDING
        # =====================================

        v1_parameter_embedding = self.model.encode(
            f"query: {v1_parameter}",
            convert_to_tensor=True
        )

        # =====================================
        # V1 DESCRIPTION EMBEDDING
        # =====================================

        v1_description_embedding = self.model.encode(
            f"query: {v1_description}",
            convert_to_tensor=True
        )

        matches = []

        # =====================================
        # LOOP THROUGH V2 PARAMETERS
        # =====================================

        for v2_parameter, v2_description in v2_data.items():

            # =====================================
            # BUSINESS FILTERS
            # =====================================

            v1_lower = v1_parameter.lower()

            v2_lower = v2_parameter.lower()

            # Benefit should not match Age

            if (
                "benefit" in v1_lower
                and
                "age" in v2_lower
            ):
                continue

            if (
                "age" in v1_lower
                and
                "benefit" in v2_lower
            ):
                continue

            # Rider should not match Benefit

            if (
                "rider" in v1_lower
                and
                "benefit" in v2_lower
            ):
                continue

            if (
                "benefit" in v1_lower
                and
                "rider" in v2_lower
            ):
                continue

            # Premium should not match Age

            if (
                "premium" in v1_lower
                and
                "age" in v2_lower
            ):
                continue

            if (
                "age" in v1_lower
                and
                "premium" in v2_lower
            ):
                continue

            # =====================================
            # PARAMETER SIMILARITY
            # =====================================

            v2_parameter_embedding = self.model.encode(
                f"passage: {v2_parameter}",
                convert_to_tensor=True
            )

            parameter_score = (

                cos_sim(
                    v1_parameter_embedding,
                    v2_parameter_embedding
                ).item()

                * 100

            )

            # =====================================
            # DESCRIPTION SIMILARITY
            # =====================================

            v2_description_embedding = self.model.encode(
                f"passage: {v2_description}",
                convert_to_tensor=True
            )

            description_score = (

                cos_sim(
                    v1_description_embedding,
                    v2_description_embedding
                ).item()

                * 100

            )

            # =====================================
            # FINAL SCORE
            # =====================================

            final_score = (

                parameter_score * 0.7

            ) + (

                description_score * 0.3

            )

            matches.append({

                "parameter":
                    v2_parameter,

                "score":
                    round(final_score, 2),

                "parameter_score":
                    round(parameter_score, 2),

                "description_score":
                    round(description_score, 2)

            })

        # =====================================
        # SAFETY CHECK
        # =====================================

        if len(matches) == 0:

            return {

                "best_match":
                    "NO MATCH FOUND",

                "confidence":
                    0,

                "business_concept":
                    "Business Semantic Matching",

                "reason":
                    "No valid business match found.",

                "review_required":
                    True,

                "top_matches":
                    []

            }

        # =====================================
        # SORT RESULTS
        # =====================================

        matches = sorted(

            matches,

            key=lambda x: x["score"],

            reverse=True

        )

        best_match = matches[0]

        # =====================================
        # DEBUG OUTPUT
        # =====================================

        print("\n" + "=" * 80)

        print(
            f"V1 Parameter: {v1_parameter}"
        )

        print("\nTop 3 Matches:")

        for match in matches[:3]:

            print(

                f"{match['parameter']} | "
                f"Final={match['score']} | "
                f"Param={match['parameter_score']} | "
                f"Desc={match['description_score']}"

            )

        print("=" * 80)

        # =====================================
        # NO MATCH THRESHOLD
        # =====================================

        if best_match["score"] < 85:

            return {

                "best_match":
                    "NO MATCH FOUND",

                "confidence":
                    round(
                        best_match["score"],
                        2
                    ),

                "business_concept":
                    "Business Semantic Matching",

                "reason":
                    (
                        "No sufficiently strong "
                        "business match found."
                    ),

                "review_required":
                    True,

                "top_matches":
                    matches[:3]

            }

        # =====================================
        # VALID MATCH
        # =====================================

        return {

            "best_match":
                best_match["parameter"],

            "confidence":
                round(
                    best_match["score"],
                    2
                ),

            "business_concept":
                "Business Semantic Matching",

            "reason":
                (
                    "Matched using semantic "
                    "parameter similarity (70%) "
                    "and semantic description "
                    "similarity (30%)."
                ),

            "review_required":
                best_match["score"] < 90,

            "top_matches":
                matches[:3]

        }

