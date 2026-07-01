class BusinessReasoner:

    def classify(
            self,
            parameter,
            description):

        parameter_text = parameter.lower()

        description_text = description.lower()

        # =====================================
        # PARAMETER NAME FIRST
        # =====================================

        if "entry age" in parameter_text:

            return "ENTRY_AGE"

        if (
            "maturity age" in parameter_text
            or "age at maturity" in parameter_text
        ):

            return "MATURITY_AGE"

        if "sum assured" in parameter_text:

            return "SUM_ASSURED"

        if "premium" in parameter_text:

            return "PREMIUM"

        if "suicide" in parameter_text:

            return "SUICIDE"

        if "surrender" in parameter_text:

            return "SURRENDER"

        if "death benefit" in parameter_text:

            return "DEATH_BENEFIT"

        if "maturity benefit" in parameter_text:

            return "MATURITY_BENEFIT"

        # =====================================
        # DESCRIPTION FALLBACK
        # =====================================

        if "suicide" in description_text:

            return "SUICIDE"

        if "surrender" in description_text:

            return "SURRENDER"

        if "death benefit" in description_text:

            return "DEATH_BENEFIT"

        if "maturity benefit" in description_text:

            return "MATURITY_BENEFIT"

        if "sum assured" in description_text:

            return "SUM_ASSURED"

        if "premium" in description_text:

            return "PREMIUM"

        return "UNKNOWN"