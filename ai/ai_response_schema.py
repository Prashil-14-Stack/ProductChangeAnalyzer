class AIResponseSchema:

    @staticmethod
    def empty_response():

        return {

            "best_match": None,

            "confidence": 0,

            "reason": "",

            "business_concept": "",

            "risk_level": "",

            "review_required": True

        }