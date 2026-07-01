class OpenAIMatcher:

    def build_prompt(
            self,
            v1_parameter,
            v1_description,
            v2_data):

        prompt = f"""
You are an insurance product analyst.

V1 Parameter:
{v1_parameter}

V1 Description:
{v1_description}

Below are V2 parameters.

Identify which V2 parameter represents the same business concept.

Return:

Best Match:
Confidence:
Reason:
"""

        for parameter, description in v2_data.items():

            prompt += f"""

V2 Parameter:
{parameter}

V2 Description:
{description}
"""

        return prompt