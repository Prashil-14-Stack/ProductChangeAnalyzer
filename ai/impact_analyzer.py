class ImpactAnalyzer:

    def analyze(
            self,
            parameter,
            added_text,
            removed_text):

        parameter_lower = (
            parameter.lower()
        )

        # -------------------------
        # AGE
        # -------------------------

        if "age" in parameter_lower:

            return {

                "Change Summary":
                    "Age related rules changed",

                "Business Impact":
                    "Eligibility and maturity calculations may change",

                "Teams":
                    "Product, Actuarial, UAT",

                "Risk":
                    "High",

                "UAT":
                    "Validate age boundaries and eligibility rules"

            }

        # -------------------------
        # SUICIDE
        # -------------------------

        elif "suicide" in parameter_lower:

            return {

                "Change Summary":
                    "Suicide benefit wording changed",

                "Business Impact":
                    "Claims processing may be impacted",

                "Teams":
                    "Claims, Compliance, UAT",

                "Risk":
                    "High",

                "UAT":
                    "Validate suicide claim scenarios"

            }

        # -------------------------
        # PREMIUM
        # -------------------------

        elif "premium" in parameter_lower:

            return {

                "Change Summary":
                    "Premium related rules changed",

                "Business Impact":
                    "Premium calculations may change",

                "Teams":
                    "Product, Finance, UAT",

                "Risk":
                    "Medium",

                "UAT":
                    "Validate premium calculations"

            }

        # -------------------------
        # DEFAULT
        # -------------------------

        return {

            "Change Summary":
                "Business rule updated",

            "Business Impact":
                "Review required",

            "Teams":
                "Product, UAT",

            "Risk":
                "Medium",

            "UAT":
                "Review business rules and create test scenarios"

        }