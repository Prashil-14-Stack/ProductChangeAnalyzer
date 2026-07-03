from services.llm_service import LLMService
import re

from config.ai_config import (
    PARAMETER_MATCH_THRESHOLD,
    PARAMETER_REVIEW_THRESHOLD
)


# ==========================================================
# Normalize Parameter Name
# ==========================================================

def normalize_parameter(parameter: str) -> str:

    parameter = (parameter or "").lower()

    parameter = re.sub(r"[\/\-_]", " ", parameter)

    parameter = re.sub(r"\s+", " ", parameter)

    return parameter.strip()


class ParameterMatcher:

    def __init__(self):

        self.llm = LLMService()

    # ======================================================
    # Match Parameter
    # ======================================================

    def match(

        self,

        source_parameter,

        source_description,

        candidates

    ):

        """
        Matching Strategy

        Step 1
            Exact parameter match

        Step 2
            GPT validation

        Step 3
            Confidence thresholds
        """

        # --------------------------------------------------
        # No Candidates
        # --------------------------------------------------

        if not candidates:

            return {

                "status": "No Match",

                "confidence": 0,

                "confidence_band": "Low",

                "matched_parameter": None,

                "matched_text": "",

                "matched_version": None,

                "matched_filename": None

            }

        # --------------------------------------------------
        # STEP 1
        # Exact Parameter Name Match
        # --------------------------------------------------

        normalized_source = normalize_parameter(

            source_parameter

        )

        for candidate in candidates:

            semantic_index = candidate["index"]

            normalized_candidate = normalize_parameter(

                semantic_index.parameter.name

            )

            if normalized_source == normalized_candidate:

                print(

                    f"✅ Exact Match Found : "

                    f"{semantic_index.parameter.name}"

                )

                return {

                    "status": "Matched",

                    "confidence": 100,

                    "confidence_band": "High",

                    "match_type": "Exact Match",

                    "matched_parameter":

                        semantic_index.parameter,

                    # Temporary (will remove after comparator migration)
                    "matched_text":

                        semantic_index.parameter.value,

                    "matched_version":

                        semantic_index.version,

                    "matched_filename":

                        semantic_index.filename

                }

        # --------------------------------------------------
        # STEP 2
        # GPT Validation
        # --------------------------------------------------

        selected_candidate = None

        for candidate in candidates:

            semantic_index = candidate["index"]

            print(

                f"🤖 Checking Candidate : "

                f"{semantic_index.parameter.name} "

                f"({candidate['similarity']}%)"

            )

            llm_candidate = {

                "parameter":

                    semantic_index.parameter.name,

                "text":

                    semantic_index.parameter.value

            }

            llm_result = self.llm.validate_parameter_match(

                source_parameter=source_parameter,

                source_description=source_description,

                candidates=[llm_candidate]

            )

            print("\n========== GPT RESPONSE ==========")
            print(llm_result)
            print("==================================\n")

            if llm_result["decision"] == "MATCH":

                selected_candidate = candidate

                break

        # --------------------------------------------------
        # No Candidate Accepted
        # --------------------------------------------------

        if selected_candidate is None:

            return {

                "status": "No Match",

                "confidence": 0,

                "confidence_band": "Low",

                "matched_parameter": None,

                "matched_text": "",

                "matched_version": None,

                "matched_filename": None

            }

        # --------------------------------------------------
        # STEP 3
        # Confidence Threshold
        # --------------------------------------------------

        similarity = selected_candidate["similarity"]

        semantic_index = selected_candidate["index"]

        if similarity >= PARAMETER_MATCH_THRESHOLD:

            status = "Matched"

            band = "High"

        elif similarity >= PARAMETER_REVIEW_THRESHOLD:

            status = "Review"

            band = "Medium"

        else:

            status = "No Match"

            band = "Low"

        # --------------------------------------------------
        # Return
        # --------------------------------------------------

        return {

            "status": status,

            "confidence": similarity,

            "confidence_band": band,

            "matched_parameter":

                semantic_index.parameter,

            # Temporary
            "matched_text":

                semantic_index.parameter.value,

            "matched_version":

                semantic_index.version,

            "matched_filename":

                semantic_index.filename

        }