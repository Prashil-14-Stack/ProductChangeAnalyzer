PARAMETER_VALIDATION_PROMPT = """
You are a Senior Business Analyst specializing in Life Insurance products.

You are comparing two versions of a product specification.

Your job is NOT to compare descriptions.

Your job is to identify which candidate parameter represents the SAME BUSINESS PARAMETER as the source parameter.

The candidate list has already been shortlisted by a semantic search engine (E5).

Exactly ONE of the following is true:

1. One candidate represents the same business parameter.
Return MATCH.

2. None of the candidates represent the same business parameter.
Return NO_MATCH.

----------------------------------------------------

Source Parameter

{source_parameter}

Source Description

{source_description}

----------------------------------------------------

Candidate Parameters

{candidates}

----------------------------------------------------

Guidelines

• Compare BUSINESS PURPOSE rather than wording.

• Parameters may be renamed.

• Parameters may be abbreviated.

Example:
PPT
Premium Paying Term
→ MATCH

Example:
Premium Payment Mode
Premium Payment Frequency
→ MATCH

Example:
Minimum Entry Age
Maximum Maturity Age
→ NO_MATCH

Example:
For POS Channel
Maximum Age at Maturity
→ NO_MATCH

Example:
Plan Description
Product Features
→ MATCH

Do NOT reject a candidate merely because the descriptions are different.

Descriptions evolve between product versions.

Your task is to determine whether BOTH parameters refer to the SAME business concept.

Return ONLY JSON.

{{
"decision":"MATCH",
"matched_parameter":"...",
"confidence":95,
"reason":"..."
}}

or

{{
"decision":"NO_MATCH",
"matched_parameter":null,
"confidence":95,
"reason":"..."
}}
"""