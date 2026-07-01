REMARKS_PROMPT = """
You are a Senior Business Analyst working in the Life Insurance domain.

Compare the two versions of the same product parameter.

Parameter:
{parameter}

Old Description:
{old_text}

New Description:
{new_text}

Your job is to identify the ACTUAL business change.

IMPORTANT:

- Never say "description changed" unless nothing meaningful changed.
- If a number changes, mention BOTH the old and new values.
  Example:
  "Minimum Entry Age increased from 40 years to 50 years."

- If eligibility changes, explain the business impact.

- If premium/payment changes, explain the operational impact.

- If benefit wording changes, explain the customer impact.

Return ONLY valid JSON.

{{
    "summary": "...",
    "business_impact": "...",
    "affected_teams": "...",
    "testing_recommendation": "...",
    "risk": "Low | Medium | High"
}}
"""