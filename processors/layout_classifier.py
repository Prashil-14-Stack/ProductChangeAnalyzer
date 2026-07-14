from dataclasses import dataclass
from typing import Dict


@dataclass
class ClassificationResult:
    """
    Result of layout classification.
    """

    block_type: str

    confidence: float

    reasons: list[str]


class LayoutClassifier:
    """
    ==========================================================
    Enterprise Layout Classification Engine

    Classifies a LayoutBlock using layout heuristics.

    This engine intentionally does NOT use AI.

    It relies only on:

        • Font Size
        • Bold Text
        • Line Count
        • Block Dimensions
        • Position
        • Capitalisation

    ==========================================================
    """

    def classify(

        self,

        block

    ) -> ClassificationResult:

        reasons = []

        confidence = 50

        text = block.text.strip()

        # ------------------------------------------------------
        # Empty Block
        # ------------------------------------------------------

        if not text:

            return ClassificationResult(

                block_type="EMPTY",

                confidence=100,

                reasons=[

                    "Block contains no text."

                ]

            )

        # ------------------------------------------------------
        # Heading
        # ------------------------------------------------------

        if (

            block.has_bold_text

            and

            block.average_font_size >= 13

            and

            block.line_count <= 2

        ):

            reasons.append(

                "Large bold text."

            )

            confidence += 40

            return ClassificationResult(

                "HEADING",

                min(confidence, 100),

                reasons

            )

        # ------------------------------------------------------
        # Bullet List
        # ------------------------------------------------------

        bullets = (

            "•",

            "-",

            "▪",

            "◦",

            "¬"

        )

        if any(

            line.text.strip().startswith(

                bullets

            )

            for line in block.lines

        ):

            reasons.append(

                "Bullet characters detected."

            )

            confidence += 35

            return ClassificationResult(

                "BULLET_LIST",

                min(confidence, 100),

                reasons

            )

        # ------------------------------------------------------
        # Table Candidate
        # ------------------------------------------------------

        if block.line_count >= 2:

            pipe_count = text.count("|")

            tab_count = text.count("\t")

            if pipe_count > 0 or tab_count > 0:

                reasons.append(

                    "Tabular separators detected."

                )

                confidence += 35

                return ClassificationResult(

                    "TABLE",

                    min(confidence, 100),

                    reasons

                )

        # ------------------------------------------------------
        # Footer
        # ------------------------------------------------------

        if (

            block.bbox[1] > 700

            and

            block.line_count <= 2

        ):

            reasons.append(

                "Located near bottom of page."

            )

            confidence += 30

            return ClassificationResult(

                "FOOTER",

                min(confidence, 100),

                reasons

            )

        # ------------------------------------------------------
        # Paragraph
        # ------------------------------------------------------

        if block.line_count >= 2:

            reasons.append(

                "Multiple lines of text."

            )

            confidence += 20

            return ClassificationResult(

                "PARAGRAPH",

                min(confidence, 100),

                reasons

            )

        # ------------------------------------------------------
        # Default
        # ------------------------------------------------------

        reasons.append(

            "No specific layout pattern detected."

        )

        return ClassificationResult(

            "UNKNOWN",

            confidence,

            reasons

        )