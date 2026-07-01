from models.product_understanding import (
    ProductUnderstanding
)

import re


class ProductUnderstandingEngine:

    def understand(
            self,
            parameter,
            description):

        parameter_lower = parameter.lower()

        description_lower = description.lower()

        # =====================================
        # BUSINESS AREA IDENTIFICATION
        # =====================================

        business_area = "General"

        if "entry age" in parameter_lower:

            business_area = "Eligibility"

        elif "maturity age" in parameter_lower:

            business_area = "Eligibility"

        elif "age at maturity" in parameter_lower:

            business_area = "Eligibility"

        elif "premium" in parameter_lower:

            business_area = "Premium"

        elif "benefit" in parameter_lower:

            business_area = "Benefits"

        elif "surrender" in parameter_lower:

            business_area = "Policy Servicing"

        elif "suicide" in parameter_lower:

            business_area = "Claims"

        elif "rider" in parameter_lower:

            business_area = "Riders"

        elif "sum assured" in parameter_lower:

            business_area = "Coverage"

        # =====================================
        # KEY RULE EXTRACTION
        # =====================================

        key_rules = []

        years_found = re.findall(
            r"\d+\s*years",
            description,
            re.IGNORECASE
        )

        for year in years_found:

            key_rules.append(
                f"Age Rule Identified: {year}"
            )

        amounts_found = re.findall(
            r"\d[\d,]*",
            description
        )

        if amounts_found:

            key_rules.append(
                f"{len(amounts_found)} numeric values identified"
            )

        if "sum assured" in description_lower:

            key_rules.append(
                "Sum Assured condition identified"
            )

        if "death benefit" in description_lower:

            key_rules.append(
                "Death Benefit rule identified"
            )

        if "maturity benefit" in description_lower:

            key_rules.append(
                "Maturity Benefit rule identified"
            )

        if "surrender" in description_lower:

            key_rules.append(
                "Surrender rule identified"
            )

        if "pos" in description_lower:

            key_rules.append(
                "POS specific condition identified"
            )

        # =====================================
        # BUSINESS UNDERSTANDING
        # =====================================

        if business_area == "Eligibility":

            business_understanding = (

                "Defines eligibility conditions "
                "applicable for policy entry "
                "or maturity."

            )

        elif business_area == "Premium":

            business_understanding = (

                "Defines premium related rules "
                "including payment or premium "
                "eligibility conditions."

            )

        elif business_area == "Benefits":

            business_understanding = (

                "Defines benefits payable "
                "under the policy."

            )

        elif business_area == "Policy Servicing":

            business_understanding = (

                "Defines servicing rules "
                "applicable during policy "
                "lifecycle."

            )

        elif business_area == "Claims":

            business_understanding = (

                "Defines claim related "
                "restrictions and conditions."

            )

        elif business_area == "Coverage":

            business_understanding = (

                "Defines coverage limits "
                "and sum assured conditions."

            )

        elif business_area == "Riders":

            business_understanding = (

                "Defines optional rider "
                "benefits available under "
                "the policy."

            )

        else:

            business_understanding = (

                "Business understanding "
                "could not be determined "
                "from the available information."

            )

        # =====================================
        # CONFIDENCE
        # =====================================

        confidence = min(
            50 + (len(key_rules) * 5),
            95
        )

        # =====================================
        # RETURN OBJECT
        # =====================================

        return ProductUnderstanding(

            parameter=parameter,

            business_understanding=
                business_understanding,

            business_area=
                business_area,

            key_rules=
                key_rules,

            confidence=
                confidence

        )