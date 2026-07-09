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
3. RapidFuzz Match

Future
------
✓ LLM Semantic Matching

==========================================================
"""

from rapidfuzz import fuzz

from knowledge.knowledge_loader import KnowledgeLoader


class ParameterMatcher:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.knowledge_loader = KnowledgeLoader()

        # Similarity threshold
        self.similarity_threshold = 90

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

        # --------------------------------------------------
        # Match Version 1 Parameters
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Remaining Version 2 Parameters = Added
        # --------------------------------------------------

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

        # ----------------------------------------------
        # Exact Canonical Match
        # ----------------------------------------------

        for parameter_v2 in candidates:

            canonical_v2 = self._canonical_name(
                parameter_v2.name
            )

            if canonical_v1 == canonical_v2:

                return parameter_v2

        # ----------------------------------------------
        # RapidFuzz Match
        # ----------------------------------------------

        best_match = None

        best_score = 0

        for parameter_v2 in candidates:

            canonical_v2 = self._canonical_name(
                parameter_v2.name
            )

            score = fuzz.token_sort_ratio(

                canonical_v1,

                canonical_v2

            )

            if score > best_score:

                best_score = score

                best_match = parameter_v2

        if best_score >= self.similarity_threshold:

            return best_match

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

        return self._normalize(canonical)

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