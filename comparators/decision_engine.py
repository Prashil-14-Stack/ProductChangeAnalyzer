from config.ai_config import DESCRIPTION_MATCH_THRESHOLD


class DecisionEngine:

    def decide(

        self,

        parameter_result,

        description_result

    ):

        if parameter_result["status"] == "No Match":

            return {

                "status": "No Match",

                "confidence": parameter_result["confidence"]

            }

        if description_result["confidence"] >= DESCRIPTION_MATCH_THRESHOLD:

            return {

                "status": "No Change",

                "confidence": description_result["confidence"]

            }

        return {

            "status": "Modified",

            "confidence": description_result["confidence"]

        }