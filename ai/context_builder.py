class ContextBuilder:

    def build_context(
            self,
            parameter,
            description):

        context = f"""
Parameter:
{parameter}

Description:
{description}
"""

        return context