import re


class ChangeDetector:

    def detect(

        self,

        old_text,

        new_text,

        description_confidence

    ):
        """
        Detects whether the parameter description
        has actually changed.

        Returns business-oriented metadata.
        """

        # ---------------------------------------
        # Exact Match
        # ---------------------------------------

        if old_text.strip() == new_text.strip():

            return {

                "change_detected": False,

                "change_type": "No Change",

                "severity": "None"

            }

        # ---------------------------------------
        # Numeric Change
        # ---------------------------------------

        old_numbers = re.findall(r"\d+(?:\.\d+)?", old_text)

        new_numbers = re.findall(r"\d+(?:\.\d+)?", new_text)

        if old_numbers != new_numbers:

            return {

                "change_detected": True,

                "change_type": "Value Changed",

                "severity": "High"

            }

        # ---------------------------------------
        # Text Changed
        # ---------------------------------------

        if description_confidence < 95:

            return {

                "change_detected": True,

                "change_type": "Description Updated",

                "severity": "Medium"

            }

        return {

            "change_detected": False,

            "change_type": "Minor Formatting",

            "severity": "Low"

        }