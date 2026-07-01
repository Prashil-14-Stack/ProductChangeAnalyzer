from services.llm_service import LLMService

from config.ai_config import (
    PARAMETER_MATCH_THRESHOLD,
    PARAMETER_REVIEW_THRESHOLD
)


class ParameterMatcher:

    def __init__(self):

        self.llm = LLMService()

    def match(

        self,

        source_parameter,

        source_description,

        candidates

    ):

        """
        Uses GPT to determine the best business parameter
        match from the Top-K semantic candidates returned
        by E5.
        """

        # -----------------------------------------
        # No candidates retrieved
        # -----------------------------------------

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

        # -----------------------------------------
        # Ask GPT to validate the candidates
        # -----------------------------------------

        llm_result = self.llm.validate_parameter_match(

            source_parameter=source_parameter,

            source_description=source_description,

            candidates=candidates

        )
        print("\n========== GPT RESPONSE ==========")
        print(llm_result)
        print("==================================\n")
        # -----------------------------------------
        # GPT says there is no business match
        # -----------------------------------------

        if llm_result["decision"] == "NO_MATCH":

            return {

                "status": "No Match",

                "confidence": llm_result.get("confidence", 0),

                "confidence_band": "Low",

                "matched_parameter": None,

                "matched_text": "",

                "matched_version": None,

                "matched_filename": None

            }

        # -----------------------------------------
        # Find GPT-selected candidate
        # -----------------------------------------

        selected_candidate = None

        for candidate in candidates:

            if candidate["parameter"] == llm_result["matched_parameter"]:

                selected_candidate = candidate

                break

        # -----------------------------------------
        # Safety check
        # -----------------------------------------

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

        # -----------------------------------------
        # Apply E5 similarity thresholds
        # -----------------------------------------

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

        # -----------------------------------------
        # Return final result
        # -----------------------------------------

        return {

            "status": status,

            "confidence": similarity,

            "confidence_band": band,

            "matched_parameter": selected_candidate["parameter"],

            "matched_text": selected_candidate["text"],

            "matched_version": selected_candidate["version"],

            "matched_filename": selected_candidate["filename"]

        }