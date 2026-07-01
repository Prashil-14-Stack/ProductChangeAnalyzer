class LLMProductUnderstanding:

    def build_prompt(
            self,
            parameter,
            description):

        prompt = f"""
You are a senior Life Insurance Product Analyst.

Analyze the following parameter.

Parameter:
{parameter}

Description:
{description}

Return:

Business Understanding:
Explain the business meaning of the parameter.

Business Area:
Examples:
Eligibility
Benefits
Premium
Claims
Coverage
Policy Servicing
Riders

Key Rules:
List all important business rules.

Confidence:
0-100
"""

        return prompt