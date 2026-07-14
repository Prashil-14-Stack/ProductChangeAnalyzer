"""
==========================================================
Enterprise Layout Classifier

Purpose
-------
Classifies every LayoutBlock into a logical
document object.

Output Types
------------
HEADING
PARAGRAPH
TABLE
LIST
FIGURE
HEADER
FOOTER
UNKNOWN

Uses weighted scoring instead of simple rules.

==========================================================
"""

import re


class LayoutClassifier:

    # -----------------------------------------------------
    # Insurance Vocabulary
    # -----------------------------------------------------

    BUSINESS_KEYWORDS = {

        "plan description",

        "entry age",

        "minimum entry age",

        "maximum entry age",

        "maturity age",

        "policy term",

        "premium payment term",

        "premium payment frequency",

        "sum assured",

        "death benefit",

        "maturity benefit",

        "surrender benefit",

        "grace period",

        "loan",

        "revival",

        "eligibility",

        "benefits",

        "options available under the product"

    }

    # =====================================================
    # Process Document
    # =====================================================

    def process(self, document):

        for page in document.pages:

            for block in page.layout_blocks:

                classification = self.classify(block)

                block.block_type = classification["type"]

                block.confidence = classification["confidence"]

                block.score = classification["score"]

                block.reasons = classification["reasons"]

        return document

    # =====================================================
    # Classify One Block
    # =====================================================

    def classify(self, block):

        score = 0

        reasons = []

        text = block.text.strip()

        words = text.split()

        # -------------------------------------------------
        # Empty
        # -------------------------------------------------

        if not text:

            return {

                "type": "EMPTY",

                "score": 100,

                "confidence": 1.0,

                "reasons": [

                    "Empty block"

                ]

            }

        # -------------------------------------------------
        # Short Text
        # -------------------------------------------------

        if len(words) <= 6:

            score += 20

            reasons.append(

                "Short text"

            )

        # -------------------------------------------------
        # Bold
        # -------------------------------------------------

        if block.has_bold_text:

            score += 25

            reasons.append(

                "Bold text"

            )

        # -------------------------------------------------
        # Larger Font
        # -------------------------------------------------

        if block.average_font_size >= 12:

            score += 20

            reasons.append(

                "Large font"

            )

        # -------------------------------------------------
        # No Full Stop
        # -------------------------------------------------

        if not text.endswith("."):

            score += 10

            reasons.append(

                "No sentence ending"

            )

        # -------------------------------------------------
        # Single Line
        # -------------------------------------------------

        if block.line_count == 1:

            score += 10

            reasons.append(

                "Single line"

            )

        # -------------------------------------------------
        # Insurance Vocabulary
        # -------------------------------------------------

        lower = text.lower()

        if lower in self.BUSINESS_KEYWORDS:

            score += 40

            reasons.append(

                "Business keyword"

            )

        # -------------------------------------------------
        # Looks like a title
        # -------------------------------------------------

        if re.match(

            r"^[A-Za-z0-9 /&()-]+$",

            text

        ):

            score += 10

            reasons.append(

                "Title pattern"

            )

        # -------------------------------------------------
        # Long paragraph penalty
        # -------------------------------------------------

        if len(words) > 40:

            score -= 30

            reasons.append(

                "Long paragraph"

            )

        # -------------------------------------------------
        # Multi-line penalty
        # -------------------------------------------------

        if block.line_count > 5:

            score -= 20

            reasons.append(

                "Multiple lines"

            )

        # =================================================
        # Decide
        # =================================================

        if score >= 70:

            block_type = "HEADING"

        elif score >= 45:

            block_type = "PARAGRAPH"

        else:

            block_type = "UNKNOWN"

        confidence = round(

            min(score, 100) / 100,

            2

        )

        return {

            "type": block_type,

            "score": score,

            "confidence": confidence,

            "reasons": reasons

        }