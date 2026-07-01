from ai.semantic_matcher import SemanticMatcher
from ai.openai_matcher import OpenAIMatcher


class MatcherFactory:

    @staticmethod
    def get_matcher(mode):

        if mode == "rule":

            return SemanticMatcher()

        elif mode == "openai":

            return OpenAIMatcher()

        raise ValueError(
            "Unknown matcher type"
        )