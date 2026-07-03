import re

from config.insurance_dictionary import ALL_BUSINESS_TERMS


class BusinessTokenizer:
    """
    =====================================================

    Product Change Analyzer V2.0

    Enterprise Business Tokenizer

    Converts raw insurance text into structured
    business-aware tokens.

    =====================================================
    """

    def __init__(self):

        self.currency_pattern = re.compile(

            r"(₹\s?\d[\d,]*(?:\.\d+)?|INR\s?\d[\d,]*(?:\.\d+)?|\$\s?\d[\d,]*(?:\.\d+)?)",

            re.IGNORECASE

        )

        self.percent_pattern = re.compile(

            r"\d+(?:\.\d+)?%"

        )

        self.date_pattern = re.compile(

            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"

            r"|"

            r"\b\d{4}-\d{2}-\d{2}\b"

        )

        self.number_pattern = re.compile(

            r"\b\d+(?:\.\d+)?\b"

        )

    # =====================================================
    # Tokenize
    # =====================================================

    def tokenize(

        self,

        text

    ):

        text = (text or "").strip()

        tokens = []

        consumed_ranges = []

        # =================================================
        # STEP 1
        # Detect Insurance Business Terms
        # =================================================

        for term in ALL_BUSINESS_TERMS:

            for match in re.finditer(

                re.escape(term),

                text,

                re.IGNORECASE

            ):

                start, end = match.span()

                consumed_ranges.append(

                    (start, end)

                )

                tokens.append({

                    "type": "BUSINESS_TERM",

                    "value": match.group(),

                    "start": start,

                    "end": end

                })

        # =================================================
        # Helper
        # =================================================

        def overlaps(start, end):

            for s, e in consumed_ranges:

                if start < e and end > s:

                    return True

            return False

        # =================================================
        # STEP 2
        # Currency
        # =================================================

        for match in self.currency_pattern.finditer(text):

            start, end = match.span()

            if overlaps(start, end):

                continue

            tokens.append({

                "type": "CURRENCY",

                "value": match.group(),

                "start": start,

                "end": end

            })

        # =================================================
        # STEP 3
        # Percentages
        # =================================================

        for match in self.percent_pattern.finditer(text):

            start, end = match.span()

            if overlaps(start, end):

                continue

            tokens.append({

                "type": "PERCENT",

                "value": match.group(),

                "start": start,

                "end": end

            })

        # =================================================
        # STEP 4
        # Dates
        # =================================================

        for match in self.date_pattern.finditer(text):

            start, end = match.span()

            if overlaps(start, end):

                continue

            tokens.append({

                "type": "DATE",

                "value": match.group(),

                "start": start,

                "end": end

            })

        # =================================================
        # STEP 5
        # Numbers
        # =================================================

        for match in self.number_pattern.finditer(text):

            start, end = match.span()

            if overlaps(start, end):

                continue

            tokens.append({

                "type": "NUMBER",

                "value": match.group(),

                "start": start,

                "end": end

            })

        # =================================================
        # STEP 6
        # Generic Words
        # =================================================

        for match in re.finditer(

            r"[A-Za-z]+" ,

            text

        ):

            start, end = match.span()

            if overlaps(start, end):

                continue

            tokens.append({

                "type": "WORD",

                "value": match.group(),

                "start": start,

                "end": end

            })

        # =================================================
        # Sort by original position
        # =================================================

        tokens.sort(

            key=lambda token: token["start"]

        )

        return tokens