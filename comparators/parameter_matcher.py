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
        Stable DOCX Parameter Matching

        Step 1
            Exact parameter name matching

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

            normalized_candidate = normalize_parameter(

                candidate["parameter"]

            )

            if normalized_source == normalized_candidate:

                print(

                    f"✅ Exact Match Found : {candidate['parameter']}"

                )

                return {

                    "status": "Matched",

                    "confidence": 100,

                    "confidence_band": "High",

                    "match_type": "Exact Match",

                    "matched_parameter": candidate["parameter"],

                    "matched_text": candidate["text"],

                    "matched_version": candidate["version"],

                    "matched_filename": candidate["filename"]

                }

        # --------------------------------------------------
        # STEP 2
        # GPT Validation
        # --------------------------------------------------

        selected_candidate = None

        for candidate in candidates:

            print(

                f"🤖 Checking Candidate : "

                f"{candidate['parameter']} "

                f"({candidate['similarity']}%)"

            )

            llm_result = self.llm.validate_parameter_match(

                source_parameter=source_parameter,

                source_description=source_description,

                candidates=[candidate]

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

            "matched_parameter": selected_candidate["parameter"],

            "matched_text": selected_candidate["text"],

            "matched_version": selected_candidate["version"],

            "matched_filename": selected_candidate["filename"]

        }