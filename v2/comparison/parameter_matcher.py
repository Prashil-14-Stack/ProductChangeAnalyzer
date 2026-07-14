"""
==========================================================
Parameter Matcher

Purpose
-------
Matches business parameters between two
ProductSpecification objects.

Matching Strategy
-----------------
1. Exact Match
2. Alias Match
3. RapidFuzz Candidate Generation
4. Semantic LLM Match

==========================================================
"""

from rapidfuzz import fuzz

from v2.knowledge.knowledge_loader import KnowledgeLoader
from v2.comparison.semantic_matcher import SemanticMatcher


class ParameterMatcher:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.knowledge_loader = KnowledgeLoader()

        self.semantic_matcher = SemanticMatcher()

        self.similarity_threshold = 90

        self.semantic_threshold = 70

    # ======================================================
    # Public
    # ======================================================

    def match(
        self,
        specification_v1,
        specification_v2
    ):

        matches = []

        unmatched_v2 = list(specification_v2.parameters)

        for parameter_v1 in specification_v1.parameters:

            parameter_v2 = self._find_best_match(

                parameter_v1,

                unmatched_v2

            )

            if parameter_v2:

                unmatched_v2.remove(parameter_v2)

            matches.append({

                "parameter_name": self._canonical_name(

                    parameter_v1.name

                ),

                "v1": parameter_v1,

                "v2": parameter_v2

            })

        for parameter_v2 in unmatched_v2:

            matches.append({

                "parameter_name": self._canonical_name(

                    parameter_v2.name

                ),

                "v1": None,

                "v2": parameter_v2

            })

        return matches

    # ======================================================
    # Matching
    # ======================================================

    def _find_best_match(

        self,

        parameter_v1,

        candidates

    ):

        canonical_v1 = self._canonical_name(

            parameter_v1.name

        )

        # --------------------------------------------------
        # Exact / Alias Match
        # --------------------------------------------------

        for parameter_v2 in candidates:

            canonical_v2 = self._canonical_name(

                parameter_v2.name

            )

            if canonical_v1 == canonical_v2:

                return parameter_v2

        # --------------------------------------------------
        # Candidate Generation
        # --------------------------------------------------

        shortlisted = []

        for parameter_v2 in candidates:

            canonical_v2 = self._canonical_name(

                parameter_v2.name

            )

            score = fuzz.token_sort_ratio(

                canonical_v1,

                canonical_v2

            )

            if score >= self.semantic_threshold:

                shortlisted.append({

                    "parameter": parameter_v2,

                    "score": score

                })

        if not shortlisted:

            return None

        shortlisted.sort(

            key=lambda item: item["score"],

            reverse=True

        )

        # --------------------------------------------------
        # High Confidence Match
        # --------------------------------------------------

        if shortlisted[0]["score"] >= self.similarity_threshold:

            return shortlisted[0]["parameter"]

        # --------------------------------------------------
        # Semantic Match
        # --------------------------------------------------

        semantic_result = self.semantic_matcher.find_best_match(

            parameter_v1,

            [

                item["parameter"]

                for item in shortlisted

            ]

        )

        if semantic_result:

            return semantic_result["parameter"]

        return None

    # ======================================================
    # Helpers
    # ======================================================

    def _canonical_name(

        self,

        parameter_name

    ):

        canonical = self.knowledge_loader.get_canonical_name(

            parameter_name

        )

        return self._normalize(

            canonical

        )

    # ------------------------------------------------------

    def _normalize(

        self,

        text

    ):

        if not text:

            return ""

        return (

            str(text)

            .strip()

            .lower()

            .replace("-", " ")

            .replace("_", " ")

        )