from openai import OpenAI
import json

from config.llm_config import (
    OPENAI_API_KEY,
    OPENAI_MODEL
)

from prompts.parameter_prompt import (
    PARAMETER_VALIDATION_PROMPT
)

from prompts.remarks_prompt import (
    REMARKS_PROMPT
)

from prompts.business_intelligence_prompt import (
    BUSINESS_INTELLIGENCE_PROMPT
)


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    # ==================================================
    # Validate Parameter Match
    # ==================================================

    def validate_parameter_match(

        self,

        source_parameter,

        source_description,

        candidates

    ):

        try:

            # ------------------------------------------
            # Convert candidates into readable text
            # ------------------------------------------

            candidate_text = ""

            for index, candidate in enumerate(candidates, start=1):

                candidate_text += (

                    f"Candidate {index}\n"

                    f"Parameter: {candidate['parameter']}\n"

                    f"Description:\n"

                    f"{candidate['text']}\n\n"

                )

            # ------------------------------------------
            # Build Prompt
            # ------------------------------------------

            prompt = PARAMETER_VALIDATION_PROMPT.format(

                source_parameter=source_parameter,

                source_description=source_description,

                candidates=candidate_text

            )

            # ------------------------------------------
            # Call GPT-4o mini
            # ------------------------------------------

            response = self.client.responses.create(

                model=OPENAI_MODEL,

                input=prompt,

                temperature=0

            )

            # ------------------------------------------
            # Extract response
            # ------------------------------------------

            content = response.output_text.strip()

            if content.startswith("```"):

                content = (

                    content

                    .replace("```json", "")

                    .replace("```", "")

                    .strip()

                )

            # ------------------------------------------
            # Parse JSON
            # ------------------------------------------

            result = json.loads(content)

            return result

        except Exception as e:

            return {

                "decision": "REVIEW",

                "matched_parameter": None,

                "confidence": 0,

                "reason": f"LLM Error: {str(e)}"

            }

    # ==================================================
    # Generate Business Remarks
    # ==================================================

    def generate_remarks(

        self,

        parameter,

        old_text,

        new_text,

        difference,

        decision

    ):
        try:

            prompt = REMARKS_PROMPT.format(

                parameter=parameter,

                old_text=old_text,

                new_text=new_text,

                difference=difference["difference_text"],

                decision=decision

            )

            response = self.client.responses.create(

                model=OPENAI_MODEL,

                input=prompt,

                temperature=0

            )

            content = response.output_text.strip()

            if content.startswith("```"):

                content = (

                    content

                    .replace("```json", "")

                    .replace("```", "")

                    .strip()

                )

            result = json.loads(content)

            remarks = (

                f"Summary: {result['summary']}\n"

                f"Business Impact: {result['business_impact']}\n"

                f"Affected Teams: {result['affected_teams']}\n"

                f"Testing: {result['testing_recommendation']}\n"

                f"Risk: {result['risk']}"

            )

            return remarks

        except Exception as e:

            return f"Unable to generate business impact: {str(e)}"
        
    # ==================================================
    # Generate Business Intelligence
    # ==================================================

    def generate_business_analysis(

        self,

        change

    ):

        """
        Generates enterprise business intelligence
        from a BusinessChange object.
        """

        try:

            prompt = BUSINESS_INTELLIGENCE_PROMPT.format(

                parameter=change.parameter,

                matched_parameter=change.matched_parameter,

                change_type=change.change_type,

                old_value=change.old_value,

                new_value=change.new_value,

                difference=change.difference_text,

                old_text=change.old_text,

                new_text=change.new_text

            )

            response = self.client.responses.create(

                model=OPENAI_MODEL,

                input=prompt,

                temperature=0

            )

            content = response.output_text.strip()

            if content.startswith("```"):

                content = (

                    content

                    .replace("```json", "")

                    .replace("```", "")

                    .strip()

                )

            result = json.loads(content)

            return result

        except Exception as e:

            print(f"\nBusiness Intelligence Error : {e}")

            return {

                "summary": "Unable to generate summary.",

                "business_impact": "",

                "customer_impact": "",

                "operational_impact": "",

                "actuarial_impact": "",

                "compliance_impact": "",

                "migration_impact": "",

                "affected_teams": [],

                "testing_recommendations": [],

                "risk": "Unknown",

                "priority": "Unknown",

                "business_criticality_score": 0,

                "customer_communication_required": False,

                "manual_review_required": True,

                "confidence": 0,

                "recommendations": [],

                "assumptions": [],

                "notes": [

                    f"LLM Error: {str(e)}"

                ]

            }