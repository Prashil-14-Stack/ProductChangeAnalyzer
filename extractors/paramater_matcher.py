from rapidfuzz import fuzz


class ParameterMatcher:

    def find_match(self, parameter, v2_parameters):

        best_match = None
        best_score = 0

        for candidate in v2_parameters:

            score = fuzz.token_sort_ratio(
                parameter.lower(),
                candidate.lower()
            )

            if score > best_score:
                best_score = score
                best_match = candidate

        return best_match, best_score