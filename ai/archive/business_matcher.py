from rapidfuzz import fuzz


class BusinessMatcher:

    def find_match(
            self,
            v1_parameter,
            v1_description,
            v2_data):

        best_match = None

        best_score = 0

        reason = ""

        for v2_parameter, v2_description in v2_data.items():

            parameter_score = fuzz.ratio(
                v1_parameter.lower(),
                v2_parameter.lower()
            )

            description_score = fuzz.ratio(
                v1_description.lower(),
                v2_description.lower()
            )

            final_score = (
                parameter_score * 0.3
                +
                description_score * 0.7
            )

            if final_score > best_score:

                best_score = final_score

                best_match = v2_parameter

                reason = (
                    f"Parameter Score="
                    f"{round(parameter_score,2)}, "
                    f"Description Score="
                    f"{round(description_score,2)}"
                )

        return {

            "best_match":
                best_match,

            "confidence":
                round(best_score, 2),

            "reason":
                reason

        }