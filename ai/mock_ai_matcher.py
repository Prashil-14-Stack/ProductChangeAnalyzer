from ai.ai_response_schema import AIResponseSchema


class MockAIMatcher:

    def find_match(
            self,
            v1_parameter,
            v1_description,
            v2_data):

        response = (
            AIResponseSchema
            .empty_response()
        )

        response["best_match"] = (
            "Mock Match"
        )

        response["confidence"] = 85

        response["reason"] = (
            "Mock AI response"
        )

        response["business_concept"] = (
            "Eligibility Rules"
        )

        response["risk_level"] = (
            "Medium"
        )

        response["review_required"] = (
            False
        )

        return response